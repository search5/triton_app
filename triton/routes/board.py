from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from flask_login import login_required, login_user, logout_user, current_user
from triton.models import db, Board, BoardComments, Member
from cerberus import Validator
from sqlalchemy import func
from formencode import htmlfill

board_app = Blueprint('triton_board', __name__)


@board_app.route("")
def board_list():
    keyword = request.args.get('keyword')

    query = db.select(Board)
    if keyword:
        query = query.filter(Board.subject.like(f'%{keyword}%'))
    query = query.order_by(db.desc(Board.seq))

    page = db.paginate(query, per_page=10)

    return render_template("board_list.jinja2", pagination=page, keyword=keyword)


@board_app.route("/<int:number>")
def board_view(number):
    article_record = db.one_or_404(db.select(Board).filter(Board.seq == number))

    article_record.hit +=  1
    db.session.commit()

    return render_template("board_view.jinja2", record=article_record)


@board_app.route('/write')
def board_write_view():
    return render_template('board_add.jinja2')


@board_app.route('/write', methods=['POST'])
def board_write_save():
    valid_schema = {'subject': {'type': 'string', 'minlength': 1, 'maxlength': 100, 'required': True},
                    'content': {'type': 'string', 'minlength': 1, 'required': True},
                    'writer_name': {'type': 'string', 'minlength': 1, 'maxlength': 20, 'required': True},
                    'password': {'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True}}
    
    # 로그인한 사용자는 작성자명과 비밀번호의 유효성을 검증하지 않도록 합니다.
    if not current_user.is_anonymous:
        valid_schema = filter(lambda x: x[0] not in ('writer_name', 'password'), valid_schema.items())
    
    v = Validator(valid_schema)

    success_result = v.validate(request.form)

    if success_result:
        # 데이터베이스에 데이터 밀어넣기
        article = Board()
        article.subject = request.form.get('subject')
        article.content = request.form.get('content')
        if current_user.is_anonymous:
            article.writer_name = request.form.get('writer_name')
            article.password = request.form.get('password')
        else:
            article.writer_name = current_user.name
            article.user_id = current_user.get_id()
        article.hit = 0
        article.modify_date = func.now()
        db.session.add(article)
        db.session.commit()

    return jsonify(success=success_result, message=v.errors, article_id=article.seq)


@board_app.route('/<int:number>/modify')
def board_modify_view(number):
    db_record = db.session.execute(db.select(Board).filter(Board.seq ==  number)).scalar_one()

    form_data = db_record.todict()
    form_data.pop('password')

    return htmlfill.render(render_template('board_modify.jinja2'), form_data)


@board_app.route('/<int:number>/modify', methods=['POST'])
def board_modify_save(number):
    valid_schema = {'subject': {'type': 'string', 'minlength': 1, 'maxlength': 100, 'required': True},
                    'content': {'type': 'string', 'minlength': 1, 'required': True},
                    'password': {'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True}}
    
    # 로그인한 사용자는 작성자명과 비밀번호의 유효성을 검증하지 않도록 합니다.
    if not current_user.is_anonymous:
        valid_schema = filter(lambda x: x[0] != 'password', valid_schema.items())

    v = Validator(valid_schema)

    success_result = v.validate(request.form)

    errors = v.errors

    if success_result:
        # 데이터베이스에 데이터 저장하기
        article = db.session.execute(db.select(Board).filter(Board.seq ==  number)).scalar_one()
        if (article.password == request.form.get('password')) or (article.user_id == current_user.get_id()):
            article.subject = request.form.get('subject')
            article.content = request.form.get('content')
            db.session.add(article)
            db.session.commit()
        else:
            success_result = False
            errors = ['데이터를 변경할 수 없습니다']

    return jsonify(success=success_result, message=errors)


@board_app.route('/<int:number>/delete', methods=['DELETE'])
def board_delete(number):
    if current_user.is_anonymous:
        valid_schema = {'password': {'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True}}
    else:
        valid_schema = {}
    
    v = Validator(valid_schema)

    success_result = v.validate(request.form)

    errors = v.errors

    if success_result:
        # 데이터베이스에 데이터 삭제하기
        article = db.session.execute(db.select(Board).filter(Board.seq == number)).scalar_one()
        if (article.password == request.form.get('password')) or (article.user_id == current_user.get_id()):
            db.session.delete(article)
            db.session.commit()
        else:
            success_result = False
            errors = ['게시물을 삭제할 수 없습니다']

    return jsonify(success=success_result, message=errors)


@board_app.route('/login')
def board_login():
    return render_template('board_login.jinja2')


@board_app.route('/login', methods=['POST'])
def board_login_proc():
    valid_schema = {'login_id': {'type': 'string', 'minlength': 1, 'maxlength': 20, 'required': True},
                    'login_pass': {'type': 'string', 'minlength': 1, 'maxlength': 40, 'required': True}}
    v = Validator(valid_schema)

    success_result = v.validate(request.form)

    errors = v.errors

    if success_result:
        login_id = request.form.get('login_id')
        login_pass = request.form.get('login_pass')

        user = db.session.execute(db.select(Member).filter(Member.id == login_id)).scalar_one()
        if not user:
            return render_template('board_login.jinja2'), 422
        elif user.password != login_pass:
            return render_template('board_login.jinja2'), 422

        login_user(user)

        return redirect('/board')
    else:
        return render_template('board_login.jinja2'), 422, (('x-errors', dict(errors)))


@board_app.route('/logout')
@login_required
def board_logout_proc():
    logout_user()
    return redirect(url_for('triton_board.board_login'))


@board_app.route("/<int:number>/comments")
def comment_list(number):
    board_comments = db.session.execute(db.select(BoardComments).filter(BoardComments.board_seq == number)).scalars()

    comments = []

    for item in board_comments:
        comment_dict = item.todict()
        comment_dict['password'] = ''
        comment_dict['editable'] = False

        comments.append(comment_dict)

    return jsonify(success=True, data=comments)


@board_app.route("/<int:number>/comments", methods=["POST"])
def comment_write(number):
    valid_schema = {'content': {'type': 'string', 'minlength': 1, 'required': True},
                    'writer_name': {'type': 'string', 'minlength': 1, 'maxlength': 20, 'required': True},
                    'password': {'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True}}
    
    # 로그인한 사용자는 작성자명과 비밀번호의 유효성을 검증하지 않도록 합니다.
    if not current_user.is_anonymous:
        valid_schema = filter(lambda x: x[0] not in ('writer_name', 'password'), valid_schema.items())

    v = Validator(valid_schema)

    success_result = v.validate(request.form)

    errors = v.errors

    seq = -1

    if success_result:
        # 데이터베이스에 데이터 밀어넣기
        comment_obj = BoardComments()
        comment_obj.board_seq = number
        comment_obj.content = request.form.get('content')
        if current_user.is_anonymous:
            comment_obj.writer_name = request.form.get('writer_name')
            comment_obj.password = request.form.get('password')
        else:
            comment_obj.writer_name = current_user.name
            comment_obj.user_id = current_user.get_id()
        comment_obj.modify_date = func.now()
        db.session.add(comment_obj)
        db.session.commit()

        seq = comment_obj.seq
    
    return redirect(url_for('triton_board.board_view', number=number)), {'x-comment_id': seq}


@board_app.route("/<int:number>/comments/<int:comment_seq>", methods=["PUT"])
def comment_modify(number, comment_seq):
    valid_schema = {'content': {'type': 'string', 'minlength': 1, 'required': True},
                    'password': {'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True}}
    
    # 로그인한 사용자는 작성자명과 비밀번호의 유효성을 검증하지 않도록 합니다.
    if not current_user.is_anonymous:
        valid_schema = filter(lambda x: x[0] not in ('password'), valid_schema.items())

    v = Validator(valid_schema)

    resp_json = request.get_json()

    success_result = v.validate(resp_json)

    errors = v.errors

    if success_result:
        # 데이터베이스에 데이터 밀어넣기
        comment_obj = db.session.execute(db.select(BoardComments).filter(BoardComments.seq == comment_seq)).scalar_one()
        if (comment_obj.password == resp_json.get('password')) or (comment_obj.user_id == current_user.get_id()):
            comment_obj.content = resp_json.get('content')
            db.session.add(comment_obj)
            db.session.commit()
    
    return jsonify(success=True)


@board_app.route("/<int:number>/comments/<int:comment_seq>", methods=["DELETE"])
def comment_delete(number, comment_seq):
    valid_schema = {'password': {'type': 'string', 'minlength': 1, 'maxlength': 30, 'required': True}}
    
    # 로그인한 사용자는 작성자명과 비밀번호의 유효성을 검증하지 않도록 합니다.
    if not current_user.is_anonymous:
        valid_schema = filter(lambda x: x[0] not in ('password'), valid_schema.items())

    v = Validator(valid_schema)

    resp_json = request.get_json()

    success_result = v.validate(resp_json)

    errors = v.errors

    if success_result:
        # 댓글 삭제
        comment_obj = db.session.execute(db.select(BoardComments).filter(BoardComments.seq == comment_seq)).scalar_one()
        if (comment_obj.password == resp_json.get('password')) or (comment_obj.user_id == current_user.get_id()):
            db.session.delete(comment_obj)
            db.session.commit()
    
    return jsonify(success=True)

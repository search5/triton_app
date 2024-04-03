import pytest
from triton.factory import create_app
from flask_login import FlaskLoginClient


@pytest.fixture()
def app():
    app = create_app("config.yaml")
    app.config.update({
        "TESTING": True,
    })
    app.test_client_class = FlaskLoginClient

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def client_user(app):
    from triton.models import db, Member

    with app.app_context():
        user = db.session.execute(db.select(Member).filter(Member.id == 'admin')).scalar_one()
        return app.test_client(user=user)


@pytest.fixture()
def write_article(client):
    req_http = client.post('/board/write', data={
        "subject": "게시물 제목",
        "content": "게시물 내용",
        "writer_name": "저자",
        "password": "1234"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_http.get_json()

    return req_http.get_json()


@pytest.fixture()
def write_comment(client, write_article):
    res = client.post(f'/board/{write_article["article_id"]}/comments', data={
        "content": "손님 상태에서 댓글 작성",
        "writer_name": "코멘트 작성자",
        "password": "1234"
    })

    return {'article_id': write_article["article_id"],
            "comment_id": res.headers.get('x-comment_id')}


@pytest.fixture()
def write_comment_loggined(client_user, write_article):
    res = client_user.post(
        f'/board/{write_article["article_id"]}/comments',
        data={
            "content": "손님 상태에서 댓글 작성",
        }
    )

    return {'article_id': write_article["article_id"],
            "comment_id": res.headers.get('x-comment_id')}


@pytest.fixture()
def write_loggined(client_user):
    # 로그인한 사용자로 게시물 추가
    req_http = client_user.post('/board/write', data={
        "subject": "로그인한 사용자가 작성한 게시물 제목",
        "content": "로그인한 사용자가 작성한 게시물 내용"
    })

    # HTTP 응답 상태 확인
    assert req_http.status == '200 OK', 'URL이 구현되지 않았습니다'

    req_json = req_http.get_json()

    # HTTP 응답 내용 확인
    assert req_http.get_json()['success'], req_json

    return req_http.get_json()

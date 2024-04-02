from flask import Blueprint, render_template, request
from triton.models import db, Board, BoardComments, Member

board_app = Blueprint('triton_board', __name__)

@board_app.route("")
def board_list():
    query = db.select(Board).order_by(db.desc(Board.seq))

    page = db.paginate(query, per_page=10)

    return render_template("board_list.jinja2", pagination=page)
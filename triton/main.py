from triton.factory import create_app
from triton.models import db
import os


app = create_app(os.getenv("TRITON_CONFIG", "config.yaml"))


@app.cli.command("dummy-data-board")
def dummy_data_board():
    """Dummy Data Insert"""
    from triton.models import Board
    from sqlalchemy import func

    for i in range(100):
        record = Board()
        record.subject = f'Test Subject {i}'
        record.content = f'Test content {i}'
        record.hit = 0
        record.writer_name = 'gdhong'
        record.password = '1234'
        record.modify_date = func.now()

        db.session.add(record)

    db.session.commit()


@app.cli.command("init-user")
def init_user():
    """Init User"""
    from triton.models import Member

    db.session.add(Member(id='admin', name='admin', password='1234'))
    db.session.commit()

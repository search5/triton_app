from triton.factory import create_app
from triton.models import db
import os


app = create_app(os.getenv("TRITON_CONFIG", "config.yaml"))


@app.cli.command("dummy-data-board")
def dummy_data_board():
    from triton.models import Board
    from sqlalchemy import func

    for i in range(100):
        record = Board()
        record.subject = f'jiho {i}'
        record.content = f'jiho content {i}'
        record.hit = 0
        record.writer_name = 'jiho'
        record.password = '1234'
        record.modify_date = func.now()

        db.session.add(record)

    db.session.commit()

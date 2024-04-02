from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import inspect
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    def todict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


db = SQLAlchemy(model_class=Base)


class Board(Base):
    seq: Mapped[int] = mapped_column(db.Identity(start=1, always=True), primary_key=True)
    subject: Mapped[str] = mapped_column(db.String(100))
    content: Mapped[Optional[str]] = mapped_column(db.Text)
    hit: Mapped[Optional[int]] = mapped_column(db.Integer)
    writer_name: Mapped[Optional[str]] = mapped_column(db.String(20))
    password: Mapped[Optional[str]] = mapped_column(db.String(30))
    user_id: Mapped[Optional[str]] = mapped_column(db.String(20))
    modify_date: Mapped[datetime] = mapped_column()


class BoardComments(Base):
    seq: Mapped[int] = mapped_column(db.Identity(start=1, always=True), primary_key=True)
    board_seq: Mapped[int] = mapped_column(db.ForeignKey('board.seq'), primary_key=True)
    content: Mapped[Optional[str]] = mapped_column(db.Text)
    writer_name: Mapped[Optional[str]] = mapped_column(db.String(20))
    password: Mapped[Optional[str]] = mapped_column(db.String(30))
    user_id: Mapped[Optional[str]] = mapped_column(db.String(20))
    modify_date: Mapped[datetime] = mapped_column()


class Member(Base, UserMixin):
    id: Mapped[str] = mapped_column(db.String(20), primary_key=True)
    name: Mapped[str] = mapped_column(db.String(20))
    password: Mapped[str] = mapped_column(db.String(40))

    @property
    def is_authenticated(self):
        return True


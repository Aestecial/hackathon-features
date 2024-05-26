from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(64), index=True, unique=True)
    password_hash: Mapped[Optional[str]] = mapped_column(sa.String(256))

    def set_password(self, password) -> str:
        self.password_hash = generate_password_hash(password)
        return

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Libraries(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    language: Mapped[Optional[str]] = mapped_column(sa.String(64), index=True)
    framework: Mapped[Optional[str]] = mapped_column(sa.String(64), index=True, unique=True)
    description: Mapped[Optional[str]] = mapped_column(sa.String(256))
    review: Mapped[Optional[str]] = mapped_column(sa.String(256))
    docs: Mapped[Optional[str]] = mapped_column(sa.String(256))
    example: Mapped[Optional[str]] = mapped_column(sa.String(256))

    def __repr__(self):
        return '<Language {}>'.format(self.language)

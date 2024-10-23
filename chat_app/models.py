from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from flask_login import UserMixin

from chat_app import db, login


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    # relationships
    sent_messages: so.Mapped[Optional[list['Message']]] = so.relationship(
        'Message', foreign_keys='Message.sender_id', backref='sender')
    received_messages: so.Mapped[Optional[list['Message']]] = so.relationship(
        'Message', foreign_keys='Message.receiver_id', backref='receiver')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Message(db.Model):
    __tablename__ = 'messages'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    message: so.Mapped[str] = so.mapped_column(sa.String(500))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))

    # Foreign keys
    sender_id = so.mapped_column(
        sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    receiver_id = so.mapped_column(
        sa.Integer, sa.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Message is {}>'.format(self.message)

# class Room():
#     __tablename__ = "rooms"
#     name: so.Mapped[str] = so.mapped_column(sa.String(150), nullable=False, unique=True)

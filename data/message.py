import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
import datetime


class Message(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'message'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name_sender = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email_sender = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    message = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    read = sqlalchemy.Column(sqlalchemy.Boolean, default=False,)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=datetime.datetime.now)
    email_recipient = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f"{self.message}"


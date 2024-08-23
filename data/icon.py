import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Icon(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'icon'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    caption = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f"{self.caption}"



import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Rest(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'rest'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    become = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    main_img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f"{self.become}"

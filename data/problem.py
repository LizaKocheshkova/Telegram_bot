import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Problem(SqlAlchemyBase):
    __tablename__ = 'problem'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fio = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    status = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return f'problem {self.id} author: {self.fio}'
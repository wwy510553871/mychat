from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime

db2 = SQLAlchemy()


class User(db2.Model):
    __tablename__ = 'chat_user'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    username = db2.Column(db2.String(64), unique=True, nullable=False)
    password = db2.Column(db2.String(128), nullable=False)
    type = db2.Column(db2.Integer, nullable=False)  # 0:普通用户, 1:管理员, 2:超管
    create_time = db2.Column(DateTime, nullable=True, default=datetime.now)
    modified_time = db2.Column(DateTime, nullable=True)

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.username

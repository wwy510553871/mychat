from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey
from datetime import datetime
import enum


db2 = SQLAlchemy()


class User(db2.Model):
    __tablename__ = 'chat_user'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    username = db2.Column(db2.String(64), unique=True, nullable=False, comment='用户名')
    password = db2.Column(db2.String(128), nullable=False, comment='密码')
    # nickname = db2.Column(db2.String(64), nullable=False, comment='昵称')
    type = db2.Column(db2.Integer, nullable=False)  # 0:普通用户, 1:管理员, 2:超管
    # portrait = db.Column(String(256), comment='头像', nullable=False)
    create_time = db2.Column(DateTime, default=datetime.now)
    modified_time = db2.Column(db2.DateTime, nullable=True, onupdate=datetime.now)
    my_chat_rooms = db2.relationship('ChatRoom', lazy='dynamic', backref='chat_user')
    # todo: 待定，用于表示现在user处于哪个房间中，可为空
    # now_in_room = db2.Column(db2.String(256), nullable=True, comment='用于表示现在user处于哪个房间中，可为空')

    def __init__(self, username, password, type):
        self.username = username
        self.password = password
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.username


class ChatRoom(db2.Model):
    """聊天室表"""
    __tablename__ = 'chat_room'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    create_user = db2.Column(db2.Integer, db2.ForeignKey('chat_user.id'), comment='创建人id')
    chat_room_users = db2.relationship('ChatRoomUser', backref='chat_room', lazy='dynamic')
    create_time = db2.Column(DateTime, default=datetime.now)
    modified_time = db2.Column(db2.DateTime, nullable=True, onupdate=datetime.now)

    def __init__(self, create_user):
        self.create_user = create_user


class ChatRoomUser(db2.Model):
    """聊天室用户中间表"""
    __tablename__ = 'chat_room_user'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    chat_room_id = db2.Column(db2.Integer, db2.ForeignKey('chat_room.id'), index=True, comment='聊天室id')
    user_id = db2.Column(db2.Integer, index=True)
    is_create_user = db2.Column(db2.Boolean, default=False, comment='角色')
    create_time = db2.Column(DateTime, default=datetime.now)
    modified_time = db2.Column(db2.DateTime, nullable=True, onupdate=datetime.now)


class ChatRoomMessage(db2.Model):
    """聊天消息表"""
    __tablename__ = 'chat_room_message'
    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    room_id = db2.Column(db2.Integer, db2.ForeignKey('chat_room.id'), comment='信息发表房间')
    user_id = db2.Column(db2.Integer, comment='信息发表人')
    msg = db2.Column(db2.String(256), comment='聊天信息')
    create_time = db2.Column(DateTime, default=datetime.now)
    modified_time = db2.Column(db2.DateTime, nullable=True, onupdate=datetime.now)


class ChatFriend(db2.Model):
    """好友审核表"""
    __tablename__ = 'chat_friend'

    class ChatFriendStatus(enum.Enum):
        """审核状态"""
        NOT_PASS = 0
        PASS = 1
        WAIT = 2

    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    self_id = db2.Column(db2.Integer, index=True, comment='自己id')
    friend_id = db2.Column(db2.Integer, index=True, comment='好友id')
    status = db2.Column(db2.SmallInteger, default=2, comment='审核状态')
    become_friends_time = db2.Column(DateTime, comment='成为好友的时间')
    room_id = db2.Column(db2.String(256), comment='房间id')
    create_time = db2.Column(DateTime, default=datetime.now)
    modified_time = db2.Column(db2.DateTime, nullable=True, onupdate=datetime.now)


class FriendMessage(db2.Model):
    """消息表"""
    __tablename__ = 'friend_message'

    class FriendMsgStatus:
        """阅读状态"""
        markRead = 0
        unRead = 1

    id = db2.Column(db2.Integer, primary_key=True, autoincrement=True)
    msg = db2.Column(db2.String(256), comment='聊天记录')
    from_user_id = db2.Column(db2.Integer, index=True, comment='发送者id')
    to_user_id = db2.Column(db2.Integer, index=True, comment='接收者id')
    room_id = db2.Column(db2.String(256), comment='房间id, 由用户id和好友id拼接而成')
    status = db2.Column(db2.SmallInteger, default=1, comment='审核状态')
    create_time = db2.Column(DateTime, default=datetime.now)
    modified_time = db2.Column(db2.DateTime, nullable=True, onupdate=datetime.now)

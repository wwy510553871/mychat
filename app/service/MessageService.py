from app.model.entity import db2, User, ChatFriend, FriendMessage
from app.model.constant import MsgHandler, msg_map
import traceback
from app.utils.socketioUtils import get_room_name
from flask import jsonify
import datetime
from sqlalchemy import or_, and_


class MessageService:

    """
    根据id和状态查找所有未读消息
    """
    def selectUnreadMessageById(self, id, status):
        try:
            res = db2.session.query(FriendMessage).filter(FriendMessage.to_user_id == id).filter(FriendMessage.status == status).all()
            return res
        except Exception as e:
            print("Exception {}".format(e))
            return None

    """
    根据my_id和好友id查找所有未读消息
    """

    def selectMessageById(self, my_id, friend_id, status):
        try:
            res = db2.session.query(FriendMessage).filter(FriendMessage.to_user_id == my_id).filter(FriendMessage.from_user_id == friend_id).filter(
                FriendMessage.status == status).all()
            return res
        except Exception as e:
            print("Exception {}".format(e))
            return None


    """
    根据id查找历史信息，并按时间顺序排列
    """
    # todo
    def selectMessageByIdOrderByTime(self, my_id, friend_id):
        try:
            res = db2.session.query(FriendMessage).filter(or_(and_(FriendMessage.to_user_id == my_id, FriendMessage.from_user_id == friend_id),
                                                              and_(FriendMessage.to_user_id == friend_id, FriendMessage.from_user_id == my_id)))\
                .order_by(FriendMessage.create_time).all()
            for msg in res:
                if msg.status == 1:
                    continue
                msg.status = 1
            db2.session.commit()
            return res

        except Exception as e:
            print("Exception {}".format(e))
            db2.session.rollback()
            return None


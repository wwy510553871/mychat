from app.model.entity import db2, User, ChatFriend
from app.model.constant import MsgHandler, msg_map
import traceback
from app.utils.friend_utils import get_room_name
from flask import jsonify
import datetime


class FriendService:

    """
    查找所有好友
    """
    def selectAllFriends(self, uid):
        try:
            friends = db2.session.query(ChatFriend).filter(ChatFriend.self_id == uid).filter(ChatFriend.status == 1).all()
            return friends
        except:
            return None

    """
    根据id查找好友（所有状态）
    """
    def selectFriendById(self, my_id, friend_id):
        try:
            return db2.session.query(ChatFriend).filter(ChatFriend.self_id == my_id).filter(ChatFriend.friend_id == friend_id).one()
        except:
            return None

    """
    根据id和type搜索好友
    """
    def selectFriendApplicationByIdAndType(self, my_id, friend_id, status):
        try:
            return db2.session.query(ChatFriend).filter(ChatFriend.self_id == my_id).filter(ChatFriend.friend_id == friend_id).filter(ChatFriend.status == status).one()
        except:
            return None

    """
    更新好友申请状态
    """
    def updateFriendApplicationStatus(self, application, status):
        try:
            application.status = status
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except:
            db2.session.rollback()
            return {'code': MsgHandler.ApplicationStatusUpdateError, 'msg': msg_map.get(MsgHandler.ApplicationStatusUpdateError)}

    """
    添加好友申请
    """
    def addFriendApplication(self, my_id, friend_id):
        try:
            room_id = get_room_name(my_id, friend_id)
            friend = ChatFriend(self_id=my_id, friend_id=friend_id, room_id=room_id)
            db2.session.add(friend)
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except Exception as e:
            print('Exception!!!!', e)
            db2.session.rollback()
            return {'code': MsgHandler.AddFriendApplicationError, 'msg': msg_map.get(MsgHandler.AddFriendApplicationError)}

    """
    审核好友申请
    """
    def checkFriendApplication(self, application, update_status):
        try:
            if update_status == 1:
                my_friend = ChatFriend(self_id=application.friend_id, friend_id=application.self_id, room_id=application.room_id)
                application.status = 1
                my_friend.status = 1
                application.become_friends_time = datetime.datetime.now()
                my_friend.become_friends_time = datetime.datetime.now()
                db2.session.add(my_friend)
                db2.session.commit()
            else:
                application.status = 0
                db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except Exception as e:
            print('Exception!!!!', e)
            db2.session.rollback()
            return {'code': MsgHandler.ApplicationStatusUpdateError, 'msg': msg_map.get(MsgHandler.ApplicationStatusUpdateError)}

    """
    发送消息
    """
    def addMsg(self, msg):
        try:
            db2.session.add(msg)
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except Exception as e:
            print('Exception!!!!', e)
            db2.session.rollback()
            return {'code': MsgHandler.SendMsgError, 'msg': msg_map.get(MsgHandler.SendMsgError)}


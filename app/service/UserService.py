from app.model.entity import db2, User
from app.model.constant import MsgHandler, msg_map
import traceback


class UserService:
    """
    添加用户
    """
    def add_user(self, user):
        try:
            db2.session.add(user)
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except:
            db2.session.rollback()
            return {'code': MsgHandler.RegisterError, 'msg': msg_map.get(MsgHandler.RegisterError)}
        # db2.session.add(user)
        # db2.session.commit()
        # return {'code': 10200, 'msg': '注册成功'}

    """
    根据username和类型查询记录
    """
    def selectByNameAndType(self, name, type):
        try:
            return db2.session.query(User).filter(User.username == name).filter(User.type == type).one()
        except:
            return None

    """
    根据username查询记录
    """
    def selectByName(self, name):
        try:
            return db2.session.query(User).filter(User.username == name).one()
        except:
            return None

    """
    根据id查询记录
    """
    def selectById(self, id):
        try:
            return db2.session.query(User).filter(User.id == id).one()
        except:
            return None

    """
    修改用户密码
    """
    def modify_password(self, uid, password):
        try:
            res = db2.session.query(User).filter(User.id == uid).one()
            res.password = password
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except:
            db2.session.rollback()
            return {'code': MsgHandler.PasswordModifyError, 'msg': msg_map.get(MsgHandler.PasswordModifyError)}

    """
    删除用户
    """
    def deleteUser(self, uid):
        try:
            db2.session.query(User).filter(User.id == uid).delete()
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except:
            db2.session.rollback()
            return {'code': MsgHandler.DeleteError, 'msg': msg_map.get(MsgHandler.DeleteError)}

    """
    查询所有普通用户
    """
    def selectAllUser(self):
        return db2.session.query(User).filter(User.type == 0).all()

    """
    查询所有用户
    """
    def selectAll(self):
        return db2.session.query(User).all()

    """
    用户状态修改，上线下线
    """
    def updataUserStatus(self, uid, user_status):
        try:
            res = db2.session.query(User).filter(User.id == uid).one()
            res.user_status = user_status
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except:
            db2.session.rollback()
            return {'code': MsgHandler.InfoUpdateError, 'msg': msg_map.get(MsgHandler.InfoUpdateError)}

    """
    保存用户sid
    """
    def addUserSid(self, uid, sid):
        try:
            res = db2.session.query(User).filter(User.id == uid).one()
            res.sid = sid
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except:
            db2.session.rollback()
            return {'code': MsgHandler.InfoUpdateError, 'msg': msg_map.get(MsgHandler.InfoUpdateError)}

    """
    加入房间
    """
    def addUserRoom(self, uid, room_id):
        try:
            res = db2.session.query(User).filter(User.id == uid).one()
            res.now_in_room = room_id
            db2.session.commit()
            return {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK)}
        except:
            db2.session.rollback()
            return {'code': MsgHandler.InfoUpdateError, 'msg': msg_map.get(MsgHandler.InfoUpdateError)}

    """
    用户状态重置，无论是正常重启还是kill后重启
    """
    def userInit(self, uid):
        try:
            res = db2.session.query(User).filter(User.id == uid).one()

            if res.now_in_room is not None:
                res.now_in_room = None
            if res.sid is not None:
                res.sid = None
            if res.user_status == 1:
                res.user_status = 0
            db2.session.commit()
        except Exception as e:
            print('!!!!!!!!!!!!!!!!Exception!!!!!!!!!!!!!!!!!!', e)
            db2.session.rollback()






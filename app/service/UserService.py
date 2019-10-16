from app.model.entity import db2, User


class UserService:
    """
    添加用户
    """
    def add_user(self, user):
        # try:
        #     db2.session.add(user)
        #     db2.session.commit()
        # except:
        #     db2.session.rollback()
        #     return {'code': 10401, 'msg': '注册失败'}
        db2.session.add(user)
        db2.session.commit()
        return {'code': 10200, 'msg': '注册成功'}

    """
    根据username和类型查询记录
    """
    def selectByName(self, name, type):
        try:
            return db2.session.query(User).filter(User.username == name).filter(User.type == type).one()
        except:
            return None


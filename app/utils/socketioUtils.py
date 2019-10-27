from flask import current_app, request


def get_room_name(self: int, friend: int) -> str:
    """获取房间名称"""
    if not isinstance(self,int) or not isinstance(friend, int):
        try:
            self = int(self)
            friend = int(friend)
        except:
            raise Exception(f'{self}&{friend}必须是一个数字!')
    return f'{self if self>friend else friend}_{self if self<friend else friend}'


# 保存socketio的sid,user_id映射
class SocketRedis(object):
    key='socketMap'

    @classmethod
    def set(cls, user: dict):
        """存储socket的映射"""
        current_app.redis.hset(cls.key, request.sid, user)

    @classmethod
    def get(cls):
        return current_app.redis.hget(cls.key, request.sid)



def get_room_name(self: int, friend: int) -> str:
    """获取房间名称"""
    if not isinstance(self,int) or not isinstance(friend, int):
        try:
            self = int(self)
            friend = int(friend)
        except:
            raise Exception(f'{self}&{friend}必须是一个数字!')
    return f'{self if self>friend else friend}_{self if self<friend else friend}'

import enum


class MsgHandler:
    OK = '2000'
    RepeatAddFriend = '4001'
    NameIsNone = '4002'
    PasswordIsNone = '4003'
    UserHasBeenRegister = '4004'
    RegisterError = '4005'
    UserHasNotBeenRegister = '4006'
    LoginError = '4007'
    PriorError = '4008'
    DeleteError = '4009'
    PasswordModifyError = '4010'
    AddFriendApplicationError = '4011'
    ApplicationIsNotExist = '4012'
    ApplicationStatusUpdateError = '4013'
    SendMsgError = '4014'


msg_map = {
    MsgHandler.OK: 'ok',
    MsgHandler.RepeatAddFriend: '重复添加好友',
    MsgHandler.NameIsNone: '用户名不可为空',
    MsgHandler.PasswordIsNone: '密码不可为空',
    MsgHandler.UserHasBeenRegister: '该用户已注册',
    MsgHandler.RegisterError: '注册失败',
    MsgHandler.UserHasNotBeenRegister: '用户未注册',
    MsgHandler.LoginError: '用户名或密码错误',
    MsgHandler.PriorError: '权限不足',
    MsgHandler.DeleteError: '删除失败',
    MsgHandler.PasswordModifyError: '修改密码失败',
    MsgHandler.AddFriendApplicationError: '发送好友申请失败',
    MsgHandler.ApplicationIsNotExist: '无此好友申请',
    MsgHandler.ApplicationStatusUpdateError: '申请状态更新失败',
    MsgHandler.SendMsgError: '发送消息失败'
}
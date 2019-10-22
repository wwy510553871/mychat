# from ... import socketio
from app.model.entity import User, db2, ChatFriend, FriendMessage
from app.model.constant import MsgHandler, msg_map
from app.view.friend import friend_blueprint
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for, jsonify
from app.service.UserService import UserService
from app.service.FriendService import FriendService
from app.service.MessageService import MessageService
from app.utils.friend_utils import get_room_name
import datetime


userService = UserService()
friendService = FriendService()
messageService = MessageService()


@friend_blueprint.route('/user/<int:my_id>/addfriend', methods=['POST'])
def add_friend_by_id_application(my_id):
    # my_id = session.get('id')
    friend_id = int(request.form['id'])
    application = friendService.selectFriendById(my_id, friend_id)
    if application:
        if application.status == 2 or application.status == 1:
            return jsonify({'code': MsgHandler.RepeatAddFriend, 'msg': msg_map.get(MsgHandler.RepeatAddFriend)})
        elif application.status == 0:
            update_res = friendService.updateFriendApplicationStatus(application, 2)
            return jsonify(update_res)
    else:
        res = friendService.addFriendApplication(my_id, friend_id)
        return jsonify(res)


@friend_blueprint.route('/user/<int:my_id>/check/<int:friend_id>', methods=['POST'])
def check_friend_application(my_id, friend_id):
    application = friendService.selectFriendApplicationByIdAndType(friend_id, my_id, 2)
    update_status = int(request.form['status'])
    if application is None:
        return jsonify({'code': MsgHandler.ApplicationIsNotExist, 'msg': msg_map.get(MsgHandler.ApplicationIsNotExist)})
    else:
        res = friendService.checkFriendApplication(application, update_status)
        return jsonify(res)


@friend_blueprint.route('/user/<int:my_id>/list', methods=['GET'])
def list_all_friends(my_id):
    my_user = userService.selectById(my_id)
    if my_user is None:
        return jsonify({'code': MsgHandler.UserHasNotBeenRegister, 'msg': msg_map.get(MsgHandler.UserHasNotBeenRegister)})
    else:
        res = friendService.selectAllFriends(my_id)
        res_ls = []
        for friend in res:
            dic = {}
            dic['friend_id'] = friend.friend_id
            dic['become_friends_time'] = friend.become_friends_time
            dic['room_id'] = friend.room_id
            friend_user = userService.selectById(dic['friend_id'])
            dic['friend_name'] = friend_user.username
            res_ls.append(dic)
        return jsonify({'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK), 'params': res_ls})


@friend_blueprint.route('/user/<int:my_id>/delete/<int:friend_id>')
def delete_friend(my_id, friend_id):
    application = friendService.selectFriendApplicationByIdAndType(my_id, friend_id, 1)
    if application is None:
        return jsonify({'code': MsgHandler.ApplicationIsNotExist, 'msg': msg_map.get(MsgHandler.ApplicationIsNotExist)})
    else:
        res = friendService.updateFriendApplicationStatus(application, 0)
        return jsonify(res)


# todo: 开发测试用
@friend_blueprint.route('/friend_login', methods=['GET', 'POST'])
def friend_login():
    if request.method == 'POST':
        session.clear()
        my_id = request.form['my_id']
        password = request.form['password']
        user = userService.selectById(my_id)
        # room_id = get_room_name(my_id, friend_id)
        if password == user.password:
            session['my_id'] = my_id
            return redirect(url_for('friend_blueprint.friend_chat'))

    # res = friendService.selectFriendApplicationByIdAndType(my_id, friend_id, 1)
    return render_template('friend_chat/index.html')

# todo: 开发测试用
@friend_blueprint.route('/friend_chat', methods=['GET'])
def friend_chat():

    if session.get('my_id') is None:
        return redirect(url_for('friend_blueprint.friend_login'))
    my_id = session.get('my_id')
    return render_template('friend_chat/chat.html', my_id=my_id)


# todo 默认返回10条
# 当打开房间时，所有未读消息均为已读
# todo 翻页？拉取上一页？
@friend_blueprint.route('/user/<int:my_id>/friend/<int:friend_id>/room')
def enter_friend_room(my_id, friend_id):
    room_id = get_room_name(my_id, friend_id)
    session['room'] = room_id
    res = messageService.selectMessageByIdOrderByTime(my_id, friend_id)
    res_ls = []
    for msg in res:
        tmp = dict()
        tmp['from_user_id'] = msg.from_user_id
        tmp['to_user_id'] = msg.to_user_id
        tmp['msg'] = msg.msg
        tmp['create_time'] = msg.create_time
        tmp['room'] = room_id
        res_ls.append(tmp)
    res_ls = res_ls[::,-1]
    return jsonify({'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK), 'params': res_ls[:10]})







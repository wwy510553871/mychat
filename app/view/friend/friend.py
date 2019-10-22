# from ... import socketio
from app.model.entity import User, db2, ChatFriend, FriendMessage
from app.model.constant import MsgHandler, msg_map
from app.view.friend import friend_blueprint
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for, jsonify
from app.service.UserService import UserService
from app.service.FriendService import FriendService
from app.utils.friend_utils import get_room_name
import datetime


userService = UserService()
friendService = FriendService()


@friend_blueprint.route('/user/<int:my_id>/addfriend', methods=['POST'])
def add_friend_by_id_application(my_id):
    # my_id = session.get('id')
    friend_id = int(request.form['id'])
    application = friendService.selectFriendById(my_id, friend_id)
    if application:
        if application.status == 2 or application.status == 1:
            return jsonify({'code': MsgHandler.RepeatAddFriend, 'msg': msg_map.get(MsgHandler.RepeatAddFriend)})
        elif application.status == 0:
            update_res = friendService.updateFriendApplicationStatus(application)
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


# @socketio.on('text', namespace='/chat')
# def chat_with_friend(message):
#     my_id = session.get('my_id')
#     friend_id = session.get('friend_id')
#     room_id = get_room_name(my_id, friend_id)
#     join_room(room_id)
#     msg = FriendMessage(msg=message['msg'], from_user_id=my_id, to_user_id=friend_id,
#                         room_id=room_id, status=0)
#     res = friendService.addMsg(msg)
#     emit('message', {'from_user_id': my_id, 'to_user_id': friend_id, 'message': message['msg']}, room=room_id)
#     return jsonify(res)


@friend_blueprint.route('/friend_login', methods=['GET', 'POST'])
def friend_login():
    if request.method == 'POST':
        session.clear()
        my_id = request.form['my_id']
        friend_id = request.form['friend_id']
        room_id = get_room_name(my_id, friend_id)
        session['my_id'] = my_id
        session['room'] = room_id
        session['friend_id'] = friend_id
        return redirect(url_for('friend_blueprint.friend_chat'))
    # res = friendService.selectFriendApplicationByIdAndType(my_id, friend_id, 1)
    return render_template('friend_chat/index.html')


@friend_blueprint.route('/friend_chat', methods=['GET'])
def friend_chat():
    room = session.get('room')
    print(session)
    print('23123213411', room)
    return render_template('friend_chat/chat.html', room=room)




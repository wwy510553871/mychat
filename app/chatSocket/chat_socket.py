from app.chatSocket import socketio
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for, jsonify, current_app, g
from flask_socketio import emit, join_room, leave_room
from app.model.entity import FriendMessage
from app.utils.socketioUtils import get_room_name
from app.service.UserService import UserService
from app.service.FriendService import FriendService
from app.service.MessageService import MessageService
from app.model.constant import MsgHandler, msg_map


userService = UserService()
messageService = MessageService()
friendService = FriendService()


@socketio.on('text', namespace='/chat')
def chat_with_friend(message):
    my_id = int(message['my_id'])
    friend_id = int(message['friend_id'])
    room_id = get_room_name(my_id, friend_id)
    # join_room(room_id)
    # print('123213412321421414112', 'my_id', my_id, 'friend_id', friend_id, 'room', room_id, 'msg', message['msg'])
    friend_user = userService.selectById(friend_id)
    if friend_user.now_in_room == room_id:
        msg_status = 1
    else:
        msg_status = 0
    msg = FriendMessage(msg=message['msg'], from_user_id=my_id, to_user_id=friend_id,
                        room_id=room_id, status=msg_status)
    res = friendService.addMsg(msg)
    # new_msgs = messageService.selectMessageById(friend_id, my_id, 0)
    emit('message', {'from_user_id': my_id, 'to_user_id': friend_id, 'msg': message['msg']}, room=room_id)

    emit('res_new_msg', {'new_msg': '有新消息', 'my_id': friend_id, 'friend_id': my_id}, room=friend_user.sid)
    return make_response(jsonify(res))


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    friend_id = int(message['friend_id'])
    my_id = int(message['my_id'])
    # my_id = session.get('my_id')
    print('!!!!!!!!!!!!!!!!!!!!!my_id: ', my_id)
    room_id = get_room_name(my_id, friend_id)
    session['room'] = room_id
    join_room(room_id)
    res = userService.addUserRoom(my_id, room_id)
    emit('status', {'msg': 'join', 'friend_id': friend_id, 'room_id': room_id}, room=room_id)
    return make_response(jsonify(res))


# todo, 消息更新


@socketio.on('user_login', namespace='/chat')
def user_login(message):
    my_id = message['my_id']
    # my_id = session.get('my_id')
    print('!!!!!!!!!!!!!!!!!!!!!my_id: ', my_id)
    sid = request.sid
    join_room(sid)
    res = userService.addUserSid(my_id, sid)
    emit('user_login_success', {'msg': str(my_id) + ' login success with sid ' + sid}, room=sid)
    return make_response(jsonify(res))


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    my_id = message['my_id']
    friend_id = message['friend_id']
    room_id = get_room_name(my_id, friend_id)
    leave_room(room_id)
    emit('status', {'msg': 'left'}, room=room_id)
    res = userService.addUserRoom(my_id, None)
    return make_response(jsonify(res))


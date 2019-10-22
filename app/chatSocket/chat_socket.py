from app.chatSocket import socketio
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for, jsonify
from flask_socketio import emit, join_room, leave_room
from app.model.entity import FriendMessage
from app.utils.friend_utils import get_room_name
from app.service.FriendService import FriendService
from app.service.MessageService import MessageService
from app.model.constant import MsgHandler, msg_map


messageService = MessageService()
friendService = FriendService()


@socketio.on('text', namespace='/chat')
def chat_with_friend(message):
    my_id = session.get('my_id')
    friend_id = session.get('friend_id')
    room_id = get_room_name(my_id, friend_id)
    # join_room(room_id)
    # print('123213412321421414112', 'my_id', my_id, 'friend_id', friend_id, 'room', room_id, 'msg', message['msg'])
    msg = FriendMessage(msg=message['msg'], from_user_id=my_id, to_user_id=friend_id,
                        room_id=room_id, status=0)
    res = friendService.addMsg(msg)
    emit('message', {'from_user_id': my_id, 'to_user_id': friend_id, 'msg': message['msg']}, room=room_id)
    return jsonify(res)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('my_id') + ' has entered the room.'}, room=room)


@socketio.on('get_friend_msgs', namespace='/chat')
def get_unread_msg_list(my_id):
    my_id = session.get('my_id')
    res = messageService.selectUnreadMessageById(my_id, 0)
    res_list = []
    users_dict = dict()
    if res is not None:
        for message in res:
            user = str(message.from_user_id)
            if user not in users_dict:
                users_dict[user] = 1
            else:
                users_dict[user] += 1
        for key, val in users_dict.items():
            res_list.append({'friend_id': key, 'msg_count': val})
        emit('res_get_friend_msgs', {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK), 'params': res_list})
    else:
        emit('res_get_friend_msgs', {'code': MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK), 'params': []})


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('my_id') + ' has left the room.'}, room=room)

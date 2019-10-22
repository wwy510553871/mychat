from app import app
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for, jsonify
from flask_socketio import emit, join_room, leave_room, SocketIO

socketio = SocketIO(app=app)
# friendService = FriendService()


# @socketio.on('text', namespace='/chat')
# def chat_with_friend(message):
#     my_id = session.get('my_id')
#     friend_id = session.get('friend_id')
#     room_id = get_room_name(my_id, friend_id)
#     join_room(room_id)
#     print('123213412321421414112', 'my_id', my_id, 'friend_id', friend_id, 'room', room_id, 'msg', message['msg'])
#     msg = FriendMessage(msg=message['msg'], from_user_id=my_id, to_user_id=friend_id,
#                         room_id=room_id, status=0)
#     res = friendService.addMsg(msg)
#     emit('message', {'from_user_id': my_id, 'to_user_id': friend_id, 'msg': message['msg']}, room=room_id)
#     return jsonify(res)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('my_id') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('my_id') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('my_id') + ' has left the room.'}, room=room)

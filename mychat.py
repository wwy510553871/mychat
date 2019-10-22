from app import create_app, socketio

app = create_app()


from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for, jsonify
from app.service.FriendService import *
from flask_socketio import SocketIO, emit, join_room, leave_room


friendService = FriendService()


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


if __name__ == '__main__':
    socketio.run(app)

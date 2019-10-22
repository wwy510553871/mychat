from app import app
from app.chatSocket.chat_socket import socketio


if __name__ == '__main__':
    socketio.run(app)

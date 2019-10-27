from app import app
from app.chatSocket.chat_socket import socketio
from flask_cors import CORS


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    socketio.run(app)

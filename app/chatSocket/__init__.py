from app import app
from flask_socketio import emit, join_room, leave_room, SocketIO
from flask_cors import CORS

CORS(app, supports_credentials=True)
socketio = SocketIO(app=app, cors_allowed_origins='*', manage_session=False)

# 存储每个user_id对应的sid
# sid_dict = dict()

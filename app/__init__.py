from app.model.entity import db2
from app.model import config
from flask import Flask, redirect, url_for, request, session, render_template
# from flask_socketio import SocketIO, join_room, emit, leave_room
from app.view.auth.auth import auth_blueprint
from app.view.manage.manage import manage_blueprint
from app.view.friend.friend import friend_blueprint


app = Flask(__name__)
app.config.from_object(config)
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

db2.init_app(app)
# db2.create_all(app=app)
app.register_blueprint(auth_blueprint)
app.register_blueprint(manage_blueprint)
app.register_blueprint(friend_blueprint)




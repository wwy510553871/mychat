from app.model.entity import User, db2
from app.model.constant import MsgHandler, msg_map
from app.view.auth import auth_blueprint

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
from app.service.UserService import UserService


userService = UserService()

# 注册
@auth_blueprint.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username is None:
        return jsonify({'code': MsgHandler.NameIsNone, 'msg': msg_map.get(MsgHandler.NameIsNone)})
    if password is None:
        return jsonify({'code': MsgHandler.PasswordIsNone, 'msg': msg_map.get(MsgHandler.PasswordIsNone)})
    if userService.selectByName(username):
        return jsonify({'code': MsgHandler.UserHasBeenRegister, 'msg': msg_map.get(MsgHandler.UserHasBeenRegister)})
    user = User(username, password, 0)
    res = userService.add_user(user)
    return jsonify(res)


# 用户登陆
@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    type = int(request.form['type'])
    user = userService.selectByNameAndType(username, type)
    if user is None:
        return jsonify({'code': MsgHandler.UserHasNotBeenRegister, 'msg': msg_map.get(MsgHandler.UserHasNotBeenRegister)})
    else:
        if password == user.password:
            userService.userInit(user.id)
            session.clear()
            session['my_id'] = user.id
            session['username'] = user.username
            session['type'] = user.type
            res = userService.updataUserStatus(user.id, 1)
            return make_response(res)
        else:
            return jsonify({'code': MsgHandler.LoginError, 'msg': msg_map.get(MsgHandler.LoginError)})












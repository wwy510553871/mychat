from app.model.entity import User, db2
from app.model.constant import MsgHandler, msg_map
from app.view.manage import manage_blueprint
from app.view.errorHandler import InvalidUsage
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for, jsonify
from app.service.UserService import UserService


userService = UserService()


# 查询所有用户
@manage_blueprint.route('/admin/<int:type>/allUsers', methods=['GET'])
def admin_all_users(type):
    res = ''
    if type == 1:
        res = userService.selectAllUser()
    elif type == 2:
        res = userService.selectAll()
    res_ls = []
    for user in res:
        dic = {}
        dic['id'] = user.id
        dic['username'] = user.username
        dic['password'] = user.password
        dic['create_time'] = user.create_time
        dic['type'] = user.type
        res_ls.append(dic)
    return jsonify({'code':  MsgHandler.OK, 'msg': msg_map.get(MsgHandler.OK), 'params': res_ls})

# 创建用户
@manage_blueprint.route('/admin/<int:type>/add', methods=['POST'])
def admin_add_user(type):
    username = request.form['username']
    password = request.form['password']
    user_type = int(request.form['type'])
    if type <= user_type:
        return jsonify({'code': MsgHandler.PriorError, 'msg': msg_map.get(MsgHandler.PriorError)})
    if username is None:
        return jsonify({'code': MsgHandler.NameIsNone, 'msg': msg_map.get(MsgHandler.NameIsNone)})
    if password is None:
        return jsonify({'code': MsgHandler.PasswordIsNone, 'msg': msg_map.get(MsgHandler.PasswordIsNone)})
    if userService.selectByName(username):
        return jsonify({'code': MsgHandler.UserHasBeenRegister, 'msg': msg_map.get(MsgHandler.UserHasBeenRegister)})
    user = User(username, password, user_type)
    res = userService.add_user(user)
    return jsonify(res)



# 删除用户
@manage_blueprint.route('/admin/<string:username>/delete/<int:id>')
def delete_user(username, id):
    admin_user = userService.selectByName(username)
    delete_user = userService.selectById(id)
    if delete_user.type >= admin_user.type:
        return jsonify({'code': MsgHandler.PriorError, 'msg': msg_map.get(MsgHandler.PriorError)})
    else:
        res = userService.deleteUser(id)
        return jsonify(res)


# 更新用户密码
@manage_blueprint.route('/admin/update/<int:id>/password/<string:password>')
def update_user(id, password):
    res = userService.modify_password(id, password)
    return jsonify(res)







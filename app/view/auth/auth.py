from app.model.entity import User, db2
from app.view.auth import auth_blueprint
from app.view.errorHandler import InvalidUsage
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for
from app.service.UserService import UserService


userService = UserService()

# 注册
@auth_blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username is None:
            raise InvalidUsage('用户名不可为空', 10401)
        if password is None:
            raise InvalidUsage('密码不可为空', 10402)
        user = User(username, password, 0)
        res = userService.add_user(user)
        print(res)
        if res['code'] != 10200:
            raise InvalidUsage('注册失败', 10403)
        else:
            return redirect(url_for('auth_blueprint.login'))
    return render_template('auth/register.html')


# 用户登陆
@auth_blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        type = int(request.form['type'])
        print('type {}'.format(type))
        user = userService.selectByName(username, type)
        if user:
            if password == user.password:
                session.clear()
                session['user_id'] = user.id
                if type == 0:
                    return redirect(url_for('index'))
                elif type == 1 or type == 2:
                    return redirect(url_for('manage_blueprint.admin'))
            else:
                raise InvalidUsage('密码错误', 10404)
    return render_template('auth/login.html')










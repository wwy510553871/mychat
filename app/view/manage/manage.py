from app.model.entity import User, db2
from app.view.manage import manage_blueprint
from app.view.errorHandler import InvalidUsage
from flask import render_template, request, make_response, send_from_directory, session, redirect, url_for
from app.service.UserService import UserService


userService = UserService()


# 登陆管理页面
@manage_blueprint.route('/admin', methods=['GET'])
def admin():
    return render_template('manage/manage.html')


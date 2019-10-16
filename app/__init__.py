from app.model.entity import db2
from app.model import config
from flask import Flask, redirect, url_for, request, session, render_template
from app.view.auth.auth import auth_blueprint
from app.view.manage.manage import manage_blueprint


def create_app():
    app = Flask(__name__, static_folder='/static', static_url_path='/static')
    app.config.from_object(config)
    app.config["SQLALCHEMY_ECHO"] = True

    @app.route('/index', methods=['GET'])
    def hello():
        return 'hello world wwy'

    db2.init_app(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(manage_blueprint)
    app.add_url_rule('/', endpoint='index', view_func=hello)

    return app
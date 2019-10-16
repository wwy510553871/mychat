import os


basedir = os.path.abspath(os.path.dirname(__file__))

USER = 'root'
PASS = 'thomas74907000'
HOST = '127.0.0.1'
PORT = '3306'
DB = 'wechat'

CHARSET = "utf8"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "THIS-A-SECRET-KEY"
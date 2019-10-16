from flask import Blueprint

errorHandler = Blueprint('errorHandler', __name__)


class InvalidUsage(Exception):
    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        res = dict()
        res['msg'] = self.message
        res['code'] = self.status_code
        return res


@errorHandler.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return error.to_dict()


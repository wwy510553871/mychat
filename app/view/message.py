import json


class Message:

    def __init__(self, msg, code, errorNum):
        self.msg = msg
        self.code = code
        self.errorNum = errorNum    # 0成功，非O失败。

    @staticmethod
    def success():
        pass

    @staticmethod
    def fail():
        pass
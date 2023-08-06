from tsdl.common import util
from tsdl.api import mm, pro


class Manual(object):
    """
    帮助手册
    """

    def __init__(self):
        self._app_manual = 'app:manual'

    def protocol(self, name: str, operation: str, security: str = None, **kwargs):
        """
        获取协议的组帧数据
        """
        parse = pro.manual(protocol=name, operation=operation, security=security)
        return util.replace(parse, **kwargs)

    def app(self, key: str, **kwargs):
        """
        获取操作APP的命令数据
        :param key:
        :return:
        """
        command = mm.get(self._app_manual, key)
        return util.replace(command, **kwargs)


manual = Manual()


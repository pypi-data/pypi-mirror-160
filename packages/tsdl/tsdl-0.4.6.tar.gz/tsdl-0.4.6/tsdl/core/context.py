import socket
from enum import Enum

from tsdl.api import em, mm
from tsdl.common import util


class TIME_UNIT(Enum):
    SECOND = 0
    MINUTE = 1
    HOUR = 2
    DAY = 3
    MONTH = 4
    YEAR = 5


class CHANNEL(Enum):
    RS485 = 'RS485'
    IR = 'IR'
    PLC = 'PLC'


class Cache(object):
    """
    缓存
    """

    def __init__(self, hostname: str):
        self._name = '{}:cache'.format(hostname)

    @property
    def name(self):
        return self._name

    def get(self, key: str):
        """
        获取键值key对应的数据从缓存中
        :param key:
        :return:
        """

        return mm.get(self._name, key)

    def set(self, key: str = None, data=None, mapping: dict = None):
        """
        保存运行时数据到缓存中
        :param key:
        :param data:
        :param mapping:
        :return:
        """
        if key is not None:
            mm.put(self._name, key, data)
        else:
            for k, v in mapping.items():
                mm.put(self._name, k, v)

    def delete(self, key: str = None):
        """
        删除缓存中运行时数据
        :param key:
        :return:
        """

        return mm.delete(self._name, key)

    def clear(self):
        return mm.clear(self.name)


class Context(object):
    """
    测试用例上下文
    """

    def __init__(self, script: str, url: str, *loops, **meters):
        self._script = script
        if script is None:
            raise Exception('Path of script file is null.')
        pfs = script.split('.')
        pfs[-1] = pfs[-1] + '.py'
        if not util.pathUtil.exist(*pfs):
            raise Exception('Script file[{}] is not exist.'.format(script))

        self._url = url
        if not util.is_valid_url(url):
            raise Exception('Format of app url is not right that should be http://IP:PORT/accept.')

        self._loops = []
        if len(loops) > 0:
            for data in loops:
                self._loops.append(self.Loop(data))

        self._cache = Cache(socket.gethostname())

        self._meters = {}
        if meters is None or len(meters) <= 0:
            raise Exception('Meters is null.')
        for pos, data in meters.items():
            self._meters[pos] = self.Meter(self._cache, pos, data)

        self._runtime = self.Runtime()

    @property
    def script(self):
        return self._script

    @property
    def url(self):
        return self._url

    @property
    def loops(self):
        return self._loops

    @property
    def meters(self):
        return self._meters

    @property
    def runtime(self):
        return self._runtime

    @property
    def cache(self):
        return self._cache

    class Loop(object):
        def __init__(self, data: dict):
            r = data.get('range')
            if r is None:
                raise Exception('Can not find range in loops. It should be like "start:end".')
            if r.find(':') <= 0:
                raise Exception('Format of range value is not right. It should be like "start:end"')
            self._range = self.Range(r)

            self._count = data.get('count')
            self._time = data.get('time')
            if self._count is None and self._time is None:
                raise Exception('Parameter of count and time both is none. One of them is not none at least.')
            if self._count is not None and self._count <= 0:
                raise Exception('Count must be more then 0.')
            if self._time is not None and type(self._time) is dict:
                self._time = self.Time(self._time)

        @property
        def range(self):
            return self._range

        @property
        def count(self):
            return self._count

        @property
        def time(self):
            return self._time

        class Range(object):
            def __init__(self, value: str):
                self._list = value.split(':')
                if len(self._list) != 2:
                    raise Exception('Length of range value after split must be 2.')
                if not self._list[0].isdigit():
                    raise Exception('Fist number of range must be decimal.')
                self._start = int(self._list[0])
                if not self._list[1].isdigit():
                    raise Exception('Fist number of range must be decimal.')
                self._end = int(self._list[1])
                if self._start > self._end:
                    raise Exception('Fist number of range must be less than second number of range.')

            @property
            def start(self):
                return self._start

            @property
            def end(self):
                return self._end

        class Time(object):
            def __init__(self, time):
                if time is not None:
                    self._start = time.get('start', None)
                    self._end = time.get('end', None)
                    self._interval = time.get('interval', None)
                    self._unit = time.get('unit', None)
                    if type(self._unit) is str:
                        self._unit = TIME_UNIT[self._unit.upper()]
                    if type(self._unit) is int:
                        self._unit = TIME_UNIT(self._unit)

            @property
            def start(self):
                return self._start

            @property
            def end(self):
                return self._end

            @property
            def interval(self):
                return self._interval

            @property
            def unit(self):
                return self._unit

    class Meter(object):
        def __init__(self, cache: Cache, pos: str, data: dict):
            self._pos = pos
            self._addr = data.get('addr')
            self._no = data.get('no')
            self._protocol = data.get('protocol')
            self._channel = {}
            chl = data.get('channel')
            if chl is not None:
                for baudrate, v in chl.items():
                    self._channel[baudrate.upper()] = v

            self._session = self.Session(cache, self.pos)

        def baudrate(self):
            return self.channel.get('baudrate'.upper())

        @property
        def pos(self):
            return self._pos

        @property
        def addr(self):
            return self._addr

        @property
        def no(self):
            return self._no

        @property
        def protocol(self):
            return self._protocol

        @property
        def channel(self):
            return self._channel

        @property
        def session(self):
            return self._session

        class Session(object):
            """
                会话 - 电表通讯加密参数
            """

            def __init__(self, cache: Cache, pos: str):
                self._cache = cache
                self._key = '{}:session'.format(pos)

                self._esam = self.ESAM()
                self._em = self.EM()

                self.__update()

            def __update(self):
                self._cache.set(self._key, data=self.to_dict())

            def to_dict(self):
                return util.to_dict(esam=self.esam.to_dict(), em=self.em.to_dict())

            def negotiate(self, get_esam_return_result: dict):
                result = get_esam_return_result['parse']['link_data']['mission']['result']
                self.esam.sn = result['esam.serial_number']
                self.esam.counter = result['esam.current_counter[1]']

                e_result = em.negotiate(self.esam.sn, self.esam.counter)
                self.em.rn = e_result['rn']
                self.em.data = e_result['data']
                self.em.mac = e_result['mac']

                self.__update()

            def verify_session(self, connect_return_result: dict):
                result = connect_return_result['parse']['link_data']['mission']['result']['connect_response_info'][
                    'security_data']
                self.esam.rn = result['server_rn']
                self.esam.mac = result['server_signature']

                e_result = em.verify_session(self.em.rn, self.esam.sn, self.esam.rn, self.esam.mac)
                self.em.iv = e_result['iv']

                self.__update()

            @property
            def esam(self):
                return self._esam

            @property
            def em(self):
                return self._em

            class ESAM(object):
                """
                    电表里的ESAM模块
                """

                def __init__(self):
                    self._sn = None
                    self._rn = None
                    self._mac = None
                    self._counter = None

                def to_dict(self):
                    return util.to_dict(sn=self.sn, counter=self.counter, rn=self.rn, mac=self.mac)

                @property
                def sn(self):
                    return self._sn

                @sn.setter
                def sn(self, value):
                    self._sn = value

                @property
                def counter(self):
                    return self._counter

                @counter.setter
                def counter(self, value):
                    self._counter = value

                @property
                def rn(self):
                    return self._rn

                @rn.setter
                def rn(self, value):
                    self._rn = value

                @property
                def mac(self):
                    return self._mac

                @mac.setter
                def mac(self, value):
                    self._mac = value

            class EM(object):
                """
                    加密机
                """

                def __init__(self):
                    self._rn = None
                    self._data = None
                    self._mac = None
                    self._iv = None  # 加密数据的密钥

                def to_dict(self):
                    return util.to_dict(rn=self.rn, data=self.data, mac=self.mac, iv=self.iv)

                @property
                def rn(self):
                    return self._rn

                @rn.setter
                def rn(self, value):
                    self._rn = value

                @property
                def data(self):
                    return self._data

                @data.setter
                def data(self, value):
                    self._data = value

                @property
                def mac(self):
                    return self._mac

                @mac.setter
                def mac(self, value):
                    self._mac = value

                @property
                def iv(self):
                    return self._iv

                @iv.setter
                def iv(self, value):
                    self._iv = value

    class Runtime(object):
        """
        运行时
        """

        def __init__(self):
            self._step = None
            self._last_result = None
            self._loop_range_start = 0
            self._loop_range_end = 0
            self._loop_index = 0
            self._loop_times = 0

        def reset_loop(self):
            self._loop_range_start = 0
            self._loop_range_end = 0
            self._loop_index = 0
            self._loop_times = 0

        @property
        def step(self):
            return self._step

        @step.setter
        def step(self, value):
            self._step = value

        @property
        def last_result(self):
            return self._last_result

        @last_result.setter
        def last_result(self, value):
            self._last_result = value

        @property
        def loop_range_start(self):
            return self._loop_range_start

        @loop_range_start.setter
        def loop_range_start(self, value):
            self._loop_range_start = value

        @property
        def loop_range_end(self):
            return self._loop_range_end

        @loop_range_end.setter
        def loop_range_end(self, value):
            self._loop_range_end = value

        @property
        def loop_index(self):
            return self._loop_index

        @loop_index.setter
        def loop_index(self, value):
            self._loop_index = value

        @property
        def loop_times(self):
            return self._loop_times

        @loop_times.setter
        def loop_times(self, value):
            self._loop_times = value

import time
from multiprocessing.managers import RemoteError
from loguru import logger
import psutil
import os
from .exceptions import SignalException
from .base import fn_get, fn_qsize, fn_put, fn_clear, EHBaseManager
from .master import signal
from .util.net import get_mac_addr


class Node(EHBaseManager):

    def __init__(self, name, address=None, authkey=None, serializer='pickle',
                 ctx=None, **kwargs):
        super().__init__(name, address=address, authkey=authkey, serializer=serializer, ctx=ctx, **kwargs)
        self.mac = get_mac_addr()
        self.fps = 0

        self._send_heartbeat_interval = 2
        self._send_heartbeat_at = 0
        self._process = psutil.Process(os.getpid())

        # 注册的队列名列表
        self.register_queue_names = []
        self.connect()
        # 发送链接成功的信号
        self.send_master_signal(signal.node_connect, name, self.mac)

    def register_queue(self, queue_name):
        """
        注册队列
        注册后的队列可以被写入和读取
        :param queue_name:
        :return:
        """
        self._register_queue(queue_name)
        self.register(fn_get(queue_name))
        self.register(fn_put(queue_name))
        self.register(fn_clear(queue_name))
        self.register(fn_qsize(queue_name))
        self.register_queue_names.append(queue_name)

    def put(self, data, queue_name):
        """
        将数据发送到指定队列
        :param data:
        :param queue_name:
        :return:
        """
        getattr(self, fn_put(queue_name))(data)

    def get(self, queue_name) -> dict:
        """
        从指定队列获取数据
        :param queue_name:
        :return:
        """
        item = getattr(self, fn_get(queue_name))()
        if item:
            return item._getvalue()

    def clear(self, queue_name):
        """
        清空指定队列
        :param queue_name:
        :return:
        """
        getattr(self, fn_clear(queue_name))()

    def qsize(self, queue_name) -> int:
        """
        获取队列的大小
        :param queue_name:
        :return:
        """
        size = getattr(self, fn_qsize(queue_name))()
        return size

    def send_master_signal(self, sig, *args, **kwargs):
        """
        向master节点发送信号
        :param sig:
        :param args:
        :param kwargs:
        :return:
        """
        if hasattr(sig, "__call__"):
            sig = sig.__name__
        _r = self._send_master_signal(sig, *args, **kwargs)
        data = _r._getvalue()
        if data['is_ok']:
            result = data['result']
            return result
        else:
            raise SignalException(str(data['msg']))

    def run(self):
        logger.info("register queue:")
        for name in self.register_queue_names:
            logger.info(f"- {name}")
        # before run生命周期回调
        self.before_run()

        while True:
            try:
                _tic = time.time()
                self._send_heartbeat()
                self.on_all_queue_process()
                # 更新fps
                self.fps = 1 / (time.time() - _tic)
            except RemoteError as e:
                """
                队列数据被消费完时会触发此异常
                """
                time.sleep(0.1)

    def _send_heartbeat(self):
        """
        发送心跳信号
        :return:
        """
        now = time.time()
        if now - self._send_heartbeat_at > self._send_heartbeat_interval:
            self.send_master_signal(signal.heartbeat, self.name, self.performance_info())
            self._send_heartbeat_at = now

    def before_run(self):
        """
        run执行前的回调 适合执行一些前置初始化
        :return:
        """
        pass

    def on_all_queue_process(self):
        """
        所有队列需要被处理的时的回调
        :return:
        """
        # 单个队列的处理回调(常用)
        for name in self.register_queue_names:
            self.on_queue_process(name)
            logger.debug(f"qsize: {self.qsize(name)}")

    def on_queue_process(self, queue_name):
        """
        队列被处理的回调入口
        :param queue_name:
        :return:
        """
        pass

    def performance_info(self) -> dict:
        """
        节点实时性能数据
        :return:
        """
        return {
            "base": {
                "fps": self.fps
            },
            "cpu": {
                "percent": self._process.cpu_percent()
            },
            "mem": {
                "percent": self._process.memory_percent(),
                "info": self._process.memory_info()
            }
        }

    def start_print(self):
        super(Node, self).start_print()
        print(f"Node ==> Master {self.address}")
        self.print_line()

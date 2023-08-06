from multiprocessing.managers import BaseManager

from queue import Queue
import time
import uuid
import os
import logging
import sys
from loguru import logger
from .util.loghandle import InterceptHandler

fn_put = lambda name: f"_{name}_put"
fn_get = lambda name: f"_{name}_get"
fn_clear = lambda name: f"_{name}_clear"
fn_qsize = lambda name: f"_{name}_qsize"


def message(data):
    return {"data": data, "at": time.time(), "id": str(uuid.uuid4())}


_logo = \
    """
      _____    _            _   _       _     
     | ____|__| | __ _  ___| | | |_   _| |__  
     |  _| / _` |/ _` |/ _ \ |_| | | | | '_ \ 
     | |__| (_| | (_| |  __/  _  | |_| | |_) |
     |_____\__,_|\__, |\___|_| |_|\__,_|_.__/ 
                 |___/                        
    """


class EQueue(Queue):

    def __init__(self):
        super().__init__()
        self.enable_put = True
        self.enable_get = True

    def put(self, item, block=True, timeout=None):
        if self.enable_put:
            super(EQueue, self).put(item, block=block, timeout=timeout)

    def get(self, block=True, timeout=None):
        if self.enable_get:
            return super(EQueue, self).get(block=block, timeout=timeout)


class EHBaseManager(BaseManager):
    def __init__(self, name, address=None, authkey=None, serializer='pickle',
                 ctx=None, **kwargs):
        super().__init__(address=address, authkey=authkey, serializer=serializer, ctx=ctx)
        self.name = name
        self.start_print()
        self.register("_register_queue", callable=self._register_queue)
        self.register("_send_master_signal", callable=self._send_master_signal)
        self._init_log(kwargs.get("log_level", "INFO"), log_dir=kwargs.get("log_dir", "logs"))

    def _init_log(self, log_level, log_dir):
        logging.basicConfig(handlers=[InterceptHandler()], level=log_level)
        logger.configure(handlers=[{"sink": sys.stderr, "level": log_level}])

        t_name = type(self).__name__
        logger.add(
            os.path.join(log_dir, f"{t_name}-{self.name}-" + "{time}.log"),
            level=log_level,
            rotation="00:00",
            retention="10 days",
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )

    def _register_queue(self, queue_name):
        """
        注册队列
        :param queue_name:
        :return:
        """

    def _send_master_signal(self, signal, *args, **kwargs):
        """
        发送信号给master
        :param signal:
        :param args:
        :param kwargs:
        :return:
        """

    def start_print(self):
        from . import __version__
        print()
        self.print_line()
        print(_logo)
        print(f"Version: {__version__}")

    @classmethod
    def print_line(cls):
        print("---" * 14)

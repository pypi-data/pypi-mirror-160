"""
系统控制相关信号
"""
import os
import psutil
from ...util.kill import kill as _kill


def kill(master):
    """
    kill master
    :param master:
    :return:
    """
    _kill(os.getpid())


def cpu_percent(master):
    """
    get cpu percent info
    :return:
    """
    pid = os.getpid()
    p = psutil.Process(pid)
    return p.cpu_percent()


def mem_percent(master):
    """
    get memory percent info
    :return:
    """
    pid = os.getpid()
    p = psutil.Process(pid)
    return p.memory_percent()


def mem_info(master):
    """
    get memory info
    :return:
    """
    pid = os.getpid()
    p = psutil.Process(pid)
    return p.memory_info()

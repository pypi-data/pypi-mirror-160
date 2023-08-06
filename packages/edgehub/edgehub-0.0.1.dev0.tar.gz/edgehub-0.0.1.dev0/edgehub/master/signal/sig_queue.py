"""
队列操作相关信号
"""
from loguru import logger
from ...base import EQueue


def list_queue(master):
    """
    list all queue
    :param master:
    :return:
    """
    return master.queue_dict.keys()


def queue_size(master, queue_name):
    """
    get queue size
    :param master:
    :param queue_name:
    :return:
    """
    if queue_name in master.queue_dict.keys():
        q: EQueue = master.queue_dict.get(queue_name)
        return q.qsize()
    else:
        logger.error(f"{queue_name} is not exist in master")
        return 0


def queue_put_switch(master, queue_name, cmd="enable"):
    """
    control the enable and disable of the put action of the queue
    :param master:
    :param queue_name:
    :param cmd:
    :return:
    """
    if queue_name in master.queue_dict.keys():
        q: EQueue = master.queue_dict.get(queue_name)
        if cmd == "enable":
            q.enable_put = True
        elif cmd == "disable":
            q.enable_put = False
        else:
            logger.error(f"put switch cmd error, cmd should be 'enable' or 'disable', but your value is {cmd}")
    else:
        logger.error(f"{queue_name} is not exist in master")


def queue_get_switch(master, queue_name, cmd="enable"):
    """
    control the enable and disable of the get action of the queue
    :param master:
    :param queue_name:
    :param cmd:
    :return:
    """
    if queue_name in master.queue_dict.keys():
        q: EQueue = master.queue_dict.get(queue_name)
        if cmd == "enable":
            q.enable_get = True
        elif cmd == "disable":
            q.enable_get = False
        else:
            logger.error(f"get switch cmd error, cmd should be 'enable' or 'disable', but your value is {cmd}")
    else:
        logger.error(f"{queue_name} is not exist in master")

"""
事件相关信号
"""
from ..node_info import NodeInfo
from loguru import logger


def node_connect(master, name, client_info):
    """
    节点连接到master
    :param master:
    :param name:
    :param client_info:
    :return:
    """
    _connect_pre_check(master, name)
    master.nodes[name] = NodeInfo(name, client_info)
    logger.info(f">>> Node [{name}]({client_info}) has successfully connected to the master!")


def heartbeat(master, name, performance_info):
    """
    心跳事件
    :param master:
    :param name:
    :param performance_info:
    :return:
    """
    # 刷新节点的时间记录
    logger.debug(f"recv {name} heartbeat")
    ni = master.nodes.get(name)
    ni.recv(performance_info)


def health_check(master, name):
    """
    检查指定节点的健康情况
    :param master:
    :param name:
    :return:
    """
    ni = master.nodes.get(name)
    return ni.is_health()


def health_check_for_all(master):
    """
    所有节点的健康检查
    :param master:
    :return:
    """
    r = {}
    for node in master.nodes.keys():
        r[node] = master.nodes[node].is_health()
    return r


def _connect_pre_check(master, name):
    # if name in master.nodes.keys():
    #     raise ConnectionError(f"{name} has already connected.")
    pass

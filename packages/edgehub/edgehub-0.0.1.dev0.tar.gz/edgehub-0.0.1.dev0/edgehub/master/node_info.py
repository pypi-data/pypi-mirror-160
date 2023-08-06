import time


class NodeInfo:
    def __init__(self, name, client_info):
        self.name = name
        self.client_info = client_info
        self._last_recv_at = time.time()
        self.performance_info = {}

    def recv(self, performance_info):
        self._last_recv_at = time.time()
        self.performance_info = performance_info

    def is_health(self, timeout_duration=10):
        """
        是否正常(默认10秒没有收到心跳 则为不正常)
        :param timeout_duration:
        :return:
        """
        return time.time() - self._last_recv_at < timeout_duration

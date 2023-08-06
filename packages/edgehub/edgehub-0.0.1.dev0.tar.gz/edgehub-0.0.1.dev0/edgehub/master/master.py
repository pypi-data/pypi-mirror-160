from ..base import fn_put, fn_get, fn_qsize, fn_clear, EHBaseManager, message, EQueue
from .signal import all_signal
from loguru import logger


class Master(EHBaseManager):

    def __init__(self, name, address=None, authkey=None, serializer='pickle',
                 ctx=None, **kwargs):
        super().__init__(name, address=address, authkey=authkey, serializer=serializer, ctx=ctx, **kwargs)
        # key node_name => val node_info obj
        self.nodes = {}
        self.queue_dict = {}

    def _send_master_signal(self, signal, *args, **kwargs):
        """
        信号执行入口
        :param signal:
        :param args:
        :param kwargs:
        :return:
        """
        logger.debug(f"receive signal: {signal} args: {args} kwargs: {kwargs}")
        is_ok = False
        result = ""
        for sig in all_signal:
            if signal == sig.__name__:
                try:
                    result = sig(self, *args, **kwargs)
                    msg = "success"
                    is_ok = True
                except Exception as e:
                    is_ok = False
                    result = ""
                    msg = str(e)
                break
        else:
            msg = f"unknown signal {signal}"
        return {"is_ok": is_ok, "result": result, "msg": msg}

    def _register_queue(self, queue_name):
        """
        注册队列
        :param queue_name:
        :return:
        """
        logger.info(f"register queue: {queue_name}")

        def put_func(data, block=True, timeout=None):
            q: EQueue = self.queue_dict.get(queue_name)
            q.put(message(data), block=block, timeout=timeout)

        def get_func(block=False, timeout=None) -> dict:
            q: EQueue = self.queue_dict.get(queue_name)
            item = q.get(block=block, timeout=timeout)
            data = item.get("data")
            return data

        def clear_func():
            q: EQueue = self.queue_dict.get(queue_name)
            while not q.empty():
                q.get_nowait()

        def qsize_func() -> int:
            q: EQueue = self.queue_dict.get(queue_name)
            return q.qsize()

        # 添加队列
        if queue_name not in self.queue_dict.keys():
            self.queue_dict[queue_name] = EQueue()
            self.register(fn_put(queue_name), callable=put_func)
            self.register(fn_get(queue_name), callable=get_func)
            self.register(fn_clear(queue_name), callable=clear_func)
            self.register(fn_qsize(queue_name), callable=qsize_func)

    def start_print(self):
        super(Master, self).start_print()
        print(f"Master {self.address}")
        self.print_line()

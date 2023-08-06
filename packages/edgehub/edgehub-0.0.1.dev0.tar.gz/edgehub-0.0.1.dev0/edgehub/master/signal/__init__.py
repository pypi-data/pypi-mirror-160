from .sig_sys import kill, cpu_percent, mem_percent, mem_info
from .sig_queue import list_queue, queue_size, queue_get_switch, queue_put_switch
from .sig_event import node_connect, heartbeat, health_check, health_check_for_all

# 信号组
signal_group = {
    "sys": [kill, cpu_percent, mem_percent, mem_info],
    "queue": [list_queue, queue_size, queue_get_switch, queue_put_switch],
    "event": [node_connect, heartbeat, health_check, health_check_for_all]
}

all_signal = []
for k in signal_group.keys():
    all_signal.extend(signal_group.get(k, []))

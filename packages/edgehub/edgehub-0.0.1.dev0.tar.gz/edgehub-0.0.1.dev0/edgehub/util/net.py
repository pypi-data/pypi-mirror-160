import uuid


def get_mac_addr():
    mac = hex(uuid.getnode())[2:]
    return mac

import socket

import zmq
from zmq.asyncio import Context


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


def from_bind2connect(addr, protocol="tcp"):
    if "tcp" in addr or "udp" in addr:
        local_ip = get_local_ip()
        port = addr.split(":")[2]
        return f"{protocol}://{local_ip}:{port}"
    return addr


def is_port_in_use(addr, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((addr, int(port))) == 0


def get_free_random_port(host=""):
    sock = socket.socket()
    sock.bind((host, 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def create_ctx(async_):
    if async_:
        ctx = Context.instance()
    else:
        ctx = zmq.Context()
    return ctx


def check_address_or_new(fulladdr) -> str:
    new_url = fulladdr
    if "tcp" in fulladdr or "udp" in fulladdr:
        _parsed = fulladdr.split("://")
        addr, port = _parsed[1].split(":")
        used = is_port_in_use(addr, port)
        if used:
            new_port = get_free_random_port(addr)
            new_url = f"{_parsed[0]}://{addr}:{new_port}"
        else:
            new_url = fulladdr

    return new_url

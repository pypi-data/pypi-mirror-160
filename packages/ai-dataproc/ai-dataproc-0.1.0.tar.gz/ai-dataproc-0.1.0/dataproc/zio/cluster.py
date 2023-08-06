import multiprocessing as mp
import os
from typing import Callable, List, Optional

import cloudpickle
import zmq
from dataproc.zio.utils import create_ctx, from_bind2connect, get_local_ip
from dataproc.zio.broker import Broker

FINISH = b"-99"


def create_worker(func: Callable, broker_addr: str):
    """ This is a wrapper which executes a function, it will pickle the result"""
    # pylint: disable=maybe-no-member
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect(broker_addr)
    print(f"Worked connected to {broker_addr}. PID {os.getpid()}")

    while True:
        message = socket.recv()
        print("Worker got message")
        if message != FINISH:
            try:
                rsp = func(message)
                bytes_data = cloudpickle.dumps(rsp)
            except Exception as e:
                bytes_data = cloudpickle.dumps(e)

            socket.send(bytes_data)
            print("Worker responded msg")
        else:
            socket.send(bytes_data)
            break


class Client:
    """ Simpler client that connects to a broker or server. It uses de REQ pattern """

    def __init__(self, ctx=None, addr="tcp://localhost:5559",  async_=True):
        # pylint: disable=maybe-no-member
        self.ctx = ctx or create_ctx(async_)
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.connect(addr)

    def send(self, msg: bytes) -> bytes:
        self.socket.send(msg)
        rsp = self.socket.recv()
        return rsp

    async def send_async(self, msg: bytes) -> bytes:
        self.socket.send(msg)
        rsp = await self.socket.recv()
        return rsp

    def close(self):
        self.socket.close()
        self.ctx.destroy()

    def close_socket(self):
        self.socket.close()


class LocalCluster:
    """ It will start a broker and a set of workers, each of them in separate
    process.
    The submit command is async, this allow multiple send of tasks.
    Each submit should open a socket because a REQ protocol requieres a response.

    Future improvments could be changing REQ by DEALER and implemented a cleaner way 
    to terminate the LocalCluster.
    """

    def __init__(self, fe="tcp://0.0.0.0:5559", be="tcp://0.0.0.0:5560",
                 num_cpus=None, async_client=True):
        self.broker = Broker(fe, be)
        self.broker.mp_start()
        self.num_cpus = num_cpus or mp.cpu_count()
        self.workers: List[mp.Process] = []
        self.ctx = create_ctx(async_client)
        self.broker_addr = from_bind2connect(self.broker.fe)
        # self.client: Client = self.create_client(async_client)

    @staticmethod
    def cpu_count():
        return mp.cpu_count()

    def start_workers(self, func: Callable):
        addr = from_bind2connect(self.broker.be)
        for _ in range(self.num_cpus):
            proc = mp.Process(target=create_worker, args=(func, addr))
            proc.start()
            self.workers.append(proc)

    def start_workers_with_state(self, worker):
        addr = from_bind2connect(self.broker.be)
        for _ in range(self.num_cpus):
            proc = mp.Process(target=worker.start, args=(addr,))
            proc.start()
            self.workers.append(proc)

    def kill_workers(self):
        for w in self.workers:
            w.kill()

    def close(self):
        self.kill_workers()
        self.broker.close()
        self.ctx.destroy()

    def get_client(self) -> Client:
        return Client(self.ctx, self.broker_addr)

    async def submit(self, data: bytes) -> bytes:
        client = self.get_client()
        rsp = await client.send_async(data)
        client.close_socket()
        return rsp

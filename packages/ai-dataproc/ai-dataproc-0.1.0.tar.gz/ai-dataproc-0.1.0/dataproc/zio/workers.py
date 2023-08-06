import multiprocessing as mp
import os
import threading
from typing import Any, Callable, Dict, Optional

import cloudpickle
import zmq
from dataproc.utils import set_logger
from dataproc.zio.broker import Broker
from dataproc.zio.cluster import Client
from dataproc.zio.utils import create_ctx, from_bind2connect, get_local_ip
from hashes.generators import Hash96

FINISH = b"-98"


def default_deserializer(data: bytes):
    rsp = cloudpickle.loads(data)
    return rsp


class LocalActorModel:
    """ LocalActorModel allows to launch workers in background, sharing a common model.
    This was thought mainly for spacy/gensim/sklearn. Some problems with pytorch may raise """

    def __init__(self, broker_back="tcp://127.0.0.1:5560",
                 broker_front="tcp://127.0.0.1:5559",
                 # control_addr="ipc:///tmp/cp",
                 control_addr="ipc:///tmp/control_plane",
                 async_client=True,
                 num_cpus=1):
        #self.broker = Broker(fe, be)
        # self.broker.mp_start()
        self.name = Hash96.time_random_string().id_hex[:-10]
        self.logger = set_logger(f"{self.__class__}.{self.name}")
        # self.logger.setLevel()
        self.logger.debug("ActorModel as %s", self.name)
        self.num_cpus = num_cpus or mp.cpu_count()

        self._broker_back = broker_back
        self._broker_front = broker_front
        self._control_addr = f"{control_addr}{self.name}"
        # self._control_addr = control_addr
        self.model = None
        self.procs = []
        self.ctx = create_ctx(async_client)
        # self.control_plane_thread = threading.Thread(target=self.control_plane)

    def init_shared_state(self, *args, **kwargs):
        """ the logic to initialize the model. Because it will be done in a process backgroudn
        for a quick memory release, the logic about how to start the model
        should be implemented here. """
        raise NotImplementedError("You should implement this method")

    def init_process_state(self, *args, **kwargs):
        """ State that only live inside of the process like a db connection """
        raise NotImplementedError("You should implement this method")

    def exit_process_state(self):
        """ State that only live inside of the process like a db connection """
        pass

    def execute(self, model, msg: bytes):
        """ This will be executed by each worker """
        raise NotImplementedError("You should implement this method")

    def create_worker(self, *args, **kwargs):
        """ This is a wrapper which executes a function, it will pickle the result"""
        # pylint: disable=maybe-no-member
        _name = f"WORKER-{os.getpid()}"
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect(self._broker_back)
        self.logger.info(
            f"{_name}: Worked connected to {self._broker_back}. PID {os.getpid()}")

        self.init_process_state(*args, **kwargs)

        while True:
            message = socket.recv()
            self.logger.debug("%s: Worker got message", _name)
            if message != FINISH:
                try:
                    rsp = self.execute(self.model, message)
                    bytes_data = cloudpickle.dumps(rsp)
                except Exception as e:
                    bytes_data = cloudpickle.dumps(e)

                socket.send(bytes_data)
                self.logger.debug(f"{_name}: Worker responded msg")
            else:
                self.logger.debug(f"{_name}: Exiting process")
                socket.send(f"{_name}: Exited".encode())
                break

        self.exit_process_state()

    def control_plane(self):
        # pylint: disable=maybe-no-member
        _name = "CONTROL-PLANE"
        ctx = create_ctx(async_=False)
        #socket = ctx.socket(zmq.SUB)
        socket = ctx.socket(zmq.REP)
        socket.bind(self._control_addr)

        self.logger.debug(f"{_name}: started in Actor {self.name}")
        while True:
            # socket.connect("tcp://127.0.0.1:5561")
            msg = socket.recv()

            self.logger.debug(f"{_name}: msg received")
            if msg == b"-99":
                self.logger.debug(f"{_name}: sending end messages to process")
                broker_socket = ctx.socket(zmq.REQ)
                broker_addr = from_bind2connect(self._broker_front)
                broker_socket.connect(broker_addr)
                for _ in self.procs:
                    broker_socket.send(b"-98")
                    msg = broker_socket.recv()
                    self.logger.debug(f"{_name}: {msg}")
                for p in self.procs:
                    self.logger.debug(f"{_name}: Killing pid {p.pid}")
                    p.kill()
                socket.send(b"Received")
                socket.close()
                broker_socket.close()
                ctx.destroy()
                self.logger.debug(f"{_name}: Context control plane deleted")
                break
            else:
                socket.send(b"Received, not kill")

    def mp_start(self, *args, **kwargs):
        print(kwargs)
        proc = mp.Process(target=self.start, args=args, kwargs=kwargs)
        proc.start()
        return proc

    def start(self, *args, **kwargs):

        self.init_shared_state(*args, **kwargs)
        print("Model started")
        print(self.model)
        # self.control_plane_thread.start()
        for x in range(self.num_cpus):
            proc = mp.Process(target=self.create_worker, args=args, kwargs=kwargs,
                              daemon=True)
            proc.start()
            self.procs.append(proc)
        t = threading.Thread(target=self.control_plane)
        t.start()
        t.join()

    def close(self):
        # pylint: disable=maybe-no-member
        ctx = create_ctx(async_=False)
        socket = ctx.socket(zmq.REQ)
        socket.connect(self._control_addr)
        socket.send(b"-99")
        msg = socket.recv()
        print("From CONTROL-PLANE, msg: ", msg)
        socket.close()
        ctx.destroy()

    def get_client(self, async_=True) -> Client:
        return Client(self.ctx, self._broker_front, async_=async_)

    async def submit(self, data: Any,
                     serializer: Optional[Callable] = None, deserializer=default_deserializer):

        if not serializer and not isinstance(data, bytes):
            raise TypeError(
                "data should be bytes or a serializer must be provided")
        client = self.get_client()
        msg = data
        if serializer:
            msg = serializer(data)

        _rsp = await client.send_async(msg)
        client.close_socket()
        rsp = _rsp
        if deserializer:
            rsp = deserializer(rsp)
        return rsp


# def actor(init_model=None, cpus=4):
#
#    model = init_model()
#
#    def decorator_actor(func):
#        @wraps(func)
#        def wrapper_func(*args, **kwargs):
#            return func(*args, **kwargs)
#        return wrapper_func
#    return decorator_actor

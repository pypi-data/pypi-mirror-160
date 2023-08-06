import logging
import multiprocessing as mp
# from logging import NullHandler
# import threading
from typing import Optional

import zmq
from dataproc.utils import set_logger
from dataproc.zio.utils import check_address_or_new
from hashes.generators import Hash96

FINISH = b"-99"


class Broker:

    def __init__(self, fe="tcp://0.0.0.0:5559", be="tcp://0.0.0.0:5560", validate_urls=True):
        self._validate = validate_urls
        if validate_urls:
            self.be = check_address_or_new(be)
            self.fe = check_address_or_new(fe)
        else:
            self.fe = fe
            self.be = be
        self.name = Hash96.time_random_string().id_hex[:-10]
        self.logger = set_logger(f"{self.__class__}.{self.name}")
        # self.logger.addHandler(NullHandler)

        self.logger.debug("Broker created as %s", self.name)

        self.bg_proc: Optional[mp.Process] = None

    def start(self):
        # pylint: disable=maybe-no-member
        if self._validate:
            self.be = check_address_or_new(self.be)
            self.fe = check_address_or_new(self.fe)
        ctx = zmq.Context()
        frontend = ctx.socket(zmq.ROUTER)
        backend = ctx.socket(zmq.DEALER)
        frontend.bind(self.fe)
        backend.bind(self.be)

        # Initialize poll set
        poller = zmq.Poller()
        poller.register(frontend, zmq.POLLIN)
        poller.register(backend, zmq.POLLIN)
        self.logger.debug("Listening front in: %s", self.fe)
        self.logger.debug("Listening back in: %s", self.be)

        while True:
            socks = dict(poller.poll())

            if socks.get(frontend) == zmq.POLLIN:
                message = frontend.recv_multipart()
                if message[2] == FINISH:
                    frontend.close()
                    backend.close()
                    ctx.destroy()
                    break
                backend.send_multipart(message)

            if socks.get(backend) == zmq.POLLIN:
                message = backend.recv_multipart()
                frontend.send_multipart(message)

    def mp_start(self):
        self.bg_proc = mp.Process(target=self.start)
        self.bg_proc.start()

    # def thread_start(self):
    #    self.thread = threading.Thread(target=self.start)
    #    self.thread.start()

    def close(self):
        self.bg_proc.kill()

# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

from typing import Callable

from ... import hagworm_slogan
from ... import __version__ as hagworm_version

from .base import install_uvloop, Utils

from ..error import catch_error
from ..interface import RunnableInterface
from ..process import Daemon
from ..asyncio.zmq import Push, Pull


SIGNAL_PORT_1 = 83310
SIGNAL_PORT_2 = 10601
HIGH_WATER_MARK = 0xffffff


class MainProcessAbstract(Daemon):

    def __init__(
            self, target: Callable, sub_process_num: int, *, keep_live: bool = False,
            push_port: int = SIGNAL_PORT_1, pull_port: int = SIGNAL_PORT_2,
            push_hwm=HIGH_WATER_MARK, pull_hwm=HIGH_WATER_MARK,
            **kwargs
    ):

        super().__init__(target, sub_process_num, keep_live=keep_live, **kwargs)

        self._push_server = Push(f'tcp://*:{push_port}', True)
        self._pull_server = Pull(f'tcp://*:{pull_port}', True)

        self._push_hwm = push_hwm
        self._pull_hwm = pull_hwm

    async def _on_message(self, message):
        raise NotImplementedError()

    async def _run(self):

        while self.is_active():

            self._check_process()

            await Utils.sleep(0.1)

            while True:

                message = await self._pull_server.recv(True)

                if message is None:
                    break
                else:
                    await self._on_message(message)

    def run(self):

        environment = Utils.environment()

        Utils.log.info(
            f'{hagworm_slogan}'
            f'hagworm {hagworm_version}\n'
            f'python {environment["python"]}\n'
            f'system {" ".join(environment["system"])}'
        )

        install_uvloop()

        self._fill_process()

        self._push_server.open(self._push_hwm)
        self._pull_server.open(self._pull_hwm)

        with catch_error():
            Utils.run_until_complete(self._run())

        self._push_server.close()
        self._pull_server.close()


class SubProcessAbstract(RunnableInterface):

    def __init__(
            self, push_port: int = SIGNAL_PORT_2, pull_port: int = SIGNAL_PORT_1,
            push_hwm=HIGH_WATER_MARK, pull_hwm=HIGH_WATER_MARK,
    ):

        self._push_client = Push(f'tcp://localhost:{push_port}')
        self._pull_client = Pull(f'tcp://localhost:{pull_port}')

        self._push_hwm = push_hwm
        self._pull_hwm = pull_hwm

        self._process_id = Utils.getpid()

    async def _run(self):
        raise NotImplementedError()

    def run(self):

        Utils.log.success(f'Started sub_process [{self._process_id}]')

        install_uvloop()

        self._push_client.open(self._push_hwm)
        self._pull_client.open(self._pull_hwm)

        Utils.run_until_complete(self._run())

        self._push_client.close()
        self._pull_client.close()

        Utils.log.success(f'Stopped sub_process [{self._process_id}]')

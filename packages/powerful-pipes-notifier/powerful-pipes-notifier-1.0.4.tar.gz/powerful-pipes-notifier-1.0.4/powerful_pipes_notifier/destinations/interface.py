from __future__ import annotations

import abc
import asyncio

from typing import List
from asyncio import Task

from ..config import RunningConfig
from ..exceptions import NotifierDeliveryException


class NotifierInterface(metaclass=abc.ABCMeta):

    def __init__(self):
        self.tasks: List[Task] = []
        self.queue = asyncio.Queue()

        # Start consumer
        self.tasks.append(
            asyncio.create_task(self.consumer())
        )

    async def join(self):
        # await asyncio.gather(*self.tasks)
        await asyncio.wait(self.tasks)

    async def notify(self, message: dict) -> None or NotifierDeliveryException:
        await self.queue.put(message)

    @classmethod
    @abc.abstractmethod
    async def open(cls, config: RunningConfig) -> NotifierInterface:
        ...

    @abc.abstractmethod
    async def consumer(self):
        raise NotImplementedError()


__all__ = ("NotifierInterface", )

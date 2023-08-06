from __future__ import annotations

import asyncio
from urllib.parse import urlparse, parse_qsl

import motor.motor_asyncio
from powerful_pipes import async_report_exception

from ..config import RunningConfig
from .interface import NotifierInterface

class MongoDBNotifier(NotifierInterface):

    def __init__(self, config: RunningConfig):
        super().__init__()

        self.debug = config.debug
        self.timeout = config.timeout
        self.max_concurrency = config.max_concurrency
        self.sem = asyncio.Semaphore(self.max_concurrency)
        # ---------------------------------------------------------------------
        # Parse mongo URI
        # ---------------------------------------------------------------------
        parsed = urlparse(config.destination_uri)

        query = dict(parse_qsl(parsed.query))

        if not all(k in query for k in ("db", "collection")):
            raise ValueError(
                "Invalid mongo configuration: db and collection are required"
            )

        db = query.pop("db")
        collection = query.pop("collection")

        # Rebuild the url without the query string
        new_queries = [f"{k}={v}" for k, v in query.items()]

        uri = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{'&'.join(new_queries)}"

        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.mongo_db = self.mongo_client[db]
        self.mongo_collection = self.mongo_db[collection]

    @classmethod
    async def open(cls, config: RunningConfig) -> NotifierInterface:
        return cls(config)

    async def store_to_mongodb(self, data: dict):
        ex = None
        message = None

        try:
            await self.mongo_collection.insert_one(data)

        except asyncio.TimeoutError as e:
            message = "Webhook: server connection timeout"
            ex = e

        except Exception as e:
            message = "Webhook: Unknown error"
            ex = e

        finally:
            self.queue.task_done()

        if ex:
            if self.debug:
                print(f"Webhook error: {message}")

            await async_report_exception(data, ex, message)

        else:
            if self.debug:
                print("Webhook done")

    async def consumer(self):

        while True:
            message = await self.queue.get()

            async with self.sem:

                self.tasks.append(asyncio.create_task(
                    self.store_to_mongodb(message)
                ))

__all__ = ("MongoDBNotifier", )

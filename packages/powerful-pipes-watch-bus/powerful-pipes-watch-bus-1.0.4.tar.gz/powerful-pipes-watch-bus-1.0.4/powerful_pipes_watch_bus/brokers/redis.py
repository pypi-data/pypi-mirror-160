from __future__ import annotations

from typing import Iterator
from urllib.parse import urlparse, parse_qsl

import redis
import orjson

from powerful_pipes import read_json

from .interface import BusInterface


class RedisBusSimpleQueue(BusInterface):

    def __init__(self, connection, queue_name: str = None):
        self.queue = queue_name
        self._connection: redis.Redis = connection

    def read_json_messages(self, queue_name: str = None) -> Iterator[dict]:

        queue = queue_name or self.queue

        while True:
            try:
                queue_name, message = self._connection.blpop(queue)
            except KeyboardInterrupt:
                return

            except:
                continue

            if message == "QUIT":
                break

            yield read_json(message)

    def send_json_message(self, data: dict, queue_name: str = None):
        queue = queue_name or self.queue

        self._connection.rpush(queue, orjson.dumps(data))

    @classmethod
    def open(cls, connection_string: str) -> RedisBusSimpleQueue:
        parsed = urlparse(connection_string)

        query = dict(parse_qsl(parsed.query))

        port = parsed.port or 6379
        host = parsed.hostname or "localhost"
        db = query.get("db", 0)
        queue = query.get("queue", None)

        o = cls(
            connection=redis.Redis(host, port, db),
            queue_name=queue
        )

        return o


class RedisBusPubSub(BusInterface):

    def __init__(self, connection, channel: str = None):
        self.channel = channel
        self._connection: redis.Redis = connection
        self.pubsub = self._connection.pubsub()

    def read_json_messages(self, channel: str = None) -> Iterator[dict]:
        channel = channel or self.channel

        if "*" in channel:
            self.pubsub.psubscribe(channel)
        else:
            self.pubsub.subscribe(channel)

        while True:

            try:
                raw_message = self.pubsub.get_message()

                if raw_message.get("type") not in ("pmessage", "message"):
                    continue

                message = raw_message.get("data")
            except KeyboardInterrupt:
                return

            except:
                continue

            if message == "QUIT":
                break

            yield read_json(message)

    def send_json_message(self, data: dict, channel: str = None):
        channel = channel or self.channel

        self._connection.publish(channel, orjson.dumps(data))

    @classmethod
    def open(cls, connection_string: str) -> RedisBusPubSub:
        parsed = urlparse(connection_string)

        query = dict(parse_qsl(parsed.query))

        port = parsed.port or 6379
        host = parsed.hostname or "localhost"
        db = query.get("db", 0)
        channel = query.get("channel", None)

        o = cls(
            connection=redis.Redis(host, port, db),
            channel=channel
        )

        return o

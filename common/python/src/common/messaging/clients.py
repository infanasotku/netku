from aio_pika.abc import AbstractQueue, AbstractExchange
import aio_pika

from common.contracts.clients import MessageInClient, MessageOutClient


class RabbitMQInClient(MessageInClient):
    def __init__(self, queue: AbstractQueue):
        self._queue = queue
        super().__init__()

    async def run(self):
        if self._handler is None:
            raise ValueError("Consumer ran without needed handler.")
        async with self._queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self._handler(message.body.decode(), headers=message.headers)


class RabbitMQOutClient(MessageOutClient):
    def __init__(self, exchange: AbstractExchange, *, routing_key: str):
        self._exchange = exchange
        self._routing_key = routing_key

    async def send(self, message, *, headers):
        await self._exchange.publish(
            aio_pika.Message(message.encode(), headers=headers),
            routing_key=self._routing_key,
        )

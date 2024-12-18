from celery import Celery


class CeleryConnector:
    def __init__(
        self,
        broker_username: str,
        broker_password: str,
        broker_host: str,
        broker_port: int,
        name: str,
    ):
        conn_string = (
            f"pyamqp://{broker_username}:{broker_password}@{broker_host}:{broker_port}/"
        )
        self.celery = Celery(
            name,
            broker=conn_string,
            backend="rpc://",
        )

    def beat(self, shedule_conf: dict):
        self.celery.conf.beat_schedule = shedule_conf
        return self.celery.Beat()

    def worker(self, /, concurrency: int):
        return self.celery.Worker(concurrency=concurrency)

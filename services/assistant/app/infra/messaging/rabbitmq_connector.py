from pika import ConnectionParameters, PlainCredentials, BlockingConnection


class RabbitMQConnector:
    def __init__(self, username: str, password: str, host: str, port: int):
        self._connection_params = ConnectionParameters(
            host=host, port=port, credentials=PlainCredentials(username, password)
        )

    def get_connection(self) -> BlockingConnection:
        return BlockingConnection(self._connection_params)

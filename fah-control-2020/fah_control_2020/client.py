from typing import Optional, List

from .connection import Connection
from .protocol import SlotCommand, ClientProtocol


class SlotConfiguration(object):
    pass


class Slot(object):
    def __init__(self, name: str, config: SlotConfiguration):
        self.name = name

    # Slot control
    def unpause(self, connection: Connection):
        connection.queue_command(f'{SlotCommand.UNPAUSE} {self.name}')

    def pause(self, connection: Connection):
        connection.queue_command(f'{SlotCommand.PAUSE} {self.name}')

    def finish(self, connection: Connection):
        connection.queue_command(f'{SlotCommand.FINISH} {self.name}')

    def on_idle(self, connection: Connection):
        connection.queue_command(f'{SlotCommand.ON_IDLE} {self.name}')

    def always_on(self, connection: Connection):
        connection.queue_command(f'{SlotCommand.ALWAYS_ON} {self.name}')


class ClientConfiguration(object):
    def __init__(self, name, address, port, password):
        self.name = name
        self.address = address
        self.port = port
        self.password = password
        self.retry_rate = 5


class Client(object):
    """
    A client is the handler of the resources on a specific connection.

    NB! Not to be confused with the single graphical client.
    """
    def __init__(self, config: ClientConfiguration):
        self.config = config
        self.selected = False
        self.ppd = 0
        self.power = ''

        self.slots: List[Optional[Slot]] = []

        self.error_messages = set()

        self.conn = Connection(
            address=self.config.address,
            port=self.config.port,
            retry_rate=self.config.retry_rate
        )

    @property
    def is_local(self):
        return self.config.address == '127.0.0.1' and self.config.name == 'local'

    def auth(self):
        self.conn.queue_command(ClientProtocol.auth_command(self.config.password))

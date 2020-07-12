import errno
import logging
import selectors
import socket
import time
from typing import Optional, List

from .protocol import SlotCommand, ClientProtocol

log = logging.getLogger(__name__)


WSAEWOULDBLOCK = 10035


class ConnectionSelector(object):
    SOCKET_BUFFER = 4096

    def __init__(self, timeout=60):
        self.sel = selectors.DefaultSelector()
        self.timeout = timeout
        self.running = False
        self._events = selectors.EVENT_READ | selectors.EVENT_WRITE

    def add_connections(self, *clients):
        for client in clients:
            client.conn.open()
            self.sel.register(
                fileobj=client.conn.socket,
                events=self._events,
                data=client
            )

    def handle_event(self, key, mask):
        sock = key.fileobj
        client = key.data
        if mask & selectors.EVENT_READ:
            client.inbound_buffer += sock.recv(self.SOCKET_BUFFER)
            if client.inbound_buffer:
                # FIXME
                pass
            else:
                self.sel.unregister(sock)
                # sock.close()
                # FIXME
        elif mask & selectors.EVENT_WRITE:
            if not client.outbound_buffer and client.outbound_messages:
                client.outbound_buffer = client.outbound_messages.pop(0)
            if client.outbound_buffer:
                log.debug('Sending %s to %s:%s', repr(client.outbound_buffer), client.address, client.port)
                sent = sock.send(client.outbound_buffer)
                client.outbound_buffer = client.outbound_buffer[sent:]

    def run(self):
        self.running = True
        while self.running:
            if not self.sel.get_map():
                # if no registered connections then quit
                self.running = False
                break

            events = self.sel.select(self.timeout)
            for key, mask in events:
                self.handle_event(key=key, mask=mask)

        self.sel.close()


class ClientConfiguration(object):
    def __init__(
            self, name: str, address: str, port: int,
            password: Optional[str] = None, retry_rate: int = 5):
        self.name = name
        self.address = address
        self.port = port
        self.password = password
        self.retry_rate = retry_rate


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

        self.outbound_messages = []
        self.outbound_buffer = b''

        self.inbound_messages = []
        self.inbound_buffer = b''

        # legacy stuff
        self.init_commands = []
        self.last_message = 0
        self.last_connect = 0
        self.connected = False

        self.socket = None
        self.fail_reason = None

    def open(self):
        self.reset()
        self.last_connect = time.time()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        err = self.socket.connect_ex((self.config.address, self.config.port))

        if err != 0 and err not in [
            errno.EINPROGRESS,
            errno.EWOULDBLOCK,
            WSAEWOULDBLOCK
        ]:
            self.fail_reason = 'connect'
            raise RuntimeError('Connection failed: ' + errno.errorcode[err])

        map(self.queue_command, self.init_commands)
        self.connected = True

    def reset(self):
        self.close()
        self.fail_reason = None
        self.last_message = 0
        self.last_connect = 0

    def close(self):
        if self.socket is not None:
            # FIXME code proper exception flow instead of catch-alls from old code.
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        self.connected = False

    @property
    def is_local(self):
        return self.config.address == '127.0.0.1' and self.config.name == 'local'

    def auth(self):
        self.queue_command(ClientProtocol.auth_command(self.config.password))

    def queue_command(self, command):
        log.debug('command: ', command)
        self.outbound_messages.append(command)


class SlotConfiguration(object):
    pass


class Slot(object):
    def __init__(self, name: str, config: SlotConfiguration):
        self.name = name

    # Slot control
    def unpause(self, client: Client):
        client.queue_command(f'{SlotCommand.UNPAUSE} {self.name}')

    def pause(self, client: Client):
        client.queue_command(f'{SlotCommand.PAUSE} {self.name}')

    def finish(self, client: Client):
        client.queue_command(f'{SlotCommand.FINISH} {self.name}')

    def on_idle(self, client: Client):
        client.queue_command(f'{SlotCommand.ON_IDLE} {self.name}')

    def always_on(self, client: Client):
        client.queue_command(f'{SlotCommand.ALWAYS_ON} {self.name}')

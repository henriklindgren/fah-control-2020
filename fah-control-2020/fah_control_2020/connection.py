import errno
import logging
import socket
import time

from .protocol import ClientProtocol

log = logging.getLogger(__name__)


class Connection(object):
    def __init__(self, address, port, password=None, retry_rate=5):
        self.address = address
        self.port = int(port)
        self.password = password
        self.init_commands = []
        self.retry_rate = retry_rate

        self.socket = None

        self.messages = []
        self.readBuf = ''
        self.writeBuf = ''
        self.fail_reason = None
        self.last_message = 0
        self.last_connect = 0

        self.connected = False

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

    def reset(self):
        self.close()
        self.messages = []
        self.readBuf = ''
        self.writeBuf = ''
        self.fail_reason = None
        self.last_message = 0
        self.last_connect = 0

    def auth(self):
        # FIXME collect all commands somewhere sane.
        self.queue_command(ClientProtocol.auth_command(self.password))

    def open(self):
        self.reset()
        self.last_connect = time.time()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        err = self.socket.connect_ex((self.address, self.port))

        if err != 0 and not err in [
            errno.EINPROGRESS,
            errno.EWOULDBLOCK,
            errno.WSAEWOULDBLOCK
        ]:
            self.fail_reason = 'connect'
            raise RuntimeError('Connection failed: ' + errno.errorcode[err])

        if self.password:
            self.auth()
        map(self.queue_command, self.init_commands)

    def queue_command(self, command):
        log.debug('command: ', command)
        self.writeBuf += command + '\n'

import time
from fah_control_2020.client import Client, ClientConfiguration


IP = '127.0.0.1'
PORT = 36330
RETRY_RATE = 0
config = ClientConfiguration(
    name='Anonymous', address=IP, port=PORT, password=None
)


def test_connecting():
    """Tests we can connect a socket and close the connection."""
    now = time.time()
    client = Client(config=config)
    client.open()
    try:
        assert client.connected
        assert client.last_connect >= now
    finally:
        client.close()


def test_login():
    """Tests we can establish a connection and login over it."""
    client = Client(config=config)
    client.open()
    try:
        client.auth()
    finally:
        client.close()

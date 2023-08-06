import base64
import threading
import time
from multiprocessing.pool import ThreadPool
from heare.config import SettingsDefinition, Setting
import logging
from pyee import EventEmitter
from websocket import WebSocketApp

from heare.client.events.message import Message, Serializer, Deserializer


__author__ = 'seanfitz'

logger = logging.getLogger(__name__)


class HeareClientSettings(SettingsDefinition):
    host = Setting(str)
    port = Setting(int)
    handler_path = Setting(str)
    ssl = Setting(bool, default=False)
    basic_user = Setting(str, default=None, required=False)
    basic_password = Setting(str, default=None, required=False)


class HeareClient(object):
    def __init__(self, config: HeareClientSettings):
        self.emitter = EventEmitter()
        self.scheme = "wss" if config.ssl.get() else "ws"
        self.host = config.host.get()
        self.port = config.port.get()
        self.handler_path = config.handler_path.get()
        self.reconnect_counter = 1

        # TODO: extract authorization
        self._auth_header = None
        user = config.basic_user.get()
        if user:
            auth_str = user + ":"
            password = config.basic_password.get()
            if password:
                auth_str += password
            self._auth_header = "Authorization: Basic %s " % str(base64.b64encode(bytes(auth_str, 'utf-8')), 'utf-8')

        self.pool = ThreadPool(10)
        self.serializer = Serializer()
        self.deserializer = Deserializer()

    def _create_new_connection(self):
        headers = []
        if self._auth_header:
            headers.append(self._auth_header)
        return WebSocketApp(
            self.scheme + "://" + self.host + ":" + str(self.port) + self.handler_path,
            header=headers,
            on_open=self._on_open,
            on_close=self._on_close,
            on_error=self._on_error,
            on_message=self._on_message)

    def _on_open(self, _):
        logger.info("Connected")
        self.emitter.emit("open")
        self.reconnect_counter = 1

    def _on_close(self, *args):
        self.emitter.emit("close")

    def _on_error(self, socket, error):
        logger.error(repr(error))
        try:
            self.emitter.emit('error', error)
            self.client.close()
        except Exception as e:
            logger.error(repr(e))
        sleep_time = self.reconnect_counter
        logger.warning(
            "Disconnecting on error, reconnecting in %d seconds." % sleep_time)
        self.reconnect_counter = min(self.reconnect_counter * 2, 60)
        time.sleep(sleep_time)

    def _on_message(self, _, message):
        try:
            self.emitter.emit('message', message)
        except Exception as e:
            logger.exception("wat")
        parsed_message = self.deserializer.deserialize(message)
        self.emitter.emit('parsed_message', parsed_message)
        self.pool.apply_async(
            self.emitter.emit, (parsed_message.message_type, parsed_message))

    def emit(self, message: Message):
        if (not self.client or not self.client.sock or
                not self.client.sock.connected):
            return
        self.client.send(self.serializer.serialize(message))

    def on(self, event_name, func):
        self.emitter.on(event_name, func)

    def once(self, event_name, func):
        self.emitter.once(event_name, func)

    def remove(self, event_name, func):
        self.emitter.remove_listener(event_name, func)

    def run_forever(self, ping_interval=1):
        while True:
            try:
                logger.info("Connecting...")
                self.client = self._create_new_connection()
                self.client.run_forever(ping_interval=ping_interval)
            except KeyboardInterrupt as _:
                logger.exception("Exiting")
                self.client.close()
                break
            except Exception as _:
                logger.exception("Error connecting to server")
                if self.client:
                    self.client.close()

        logger.info("Client run_forever complete.")

    def close(self):
        self.client.close()


def main():
    logging.basicConfig(level=logging.DEBUG)
    settings = HeareClientSettings.load()
    client = HeareClient(settings)

    def echo(message):
        logger.info(message)

    client.on('message', echo)
    threading.Thread(target=client.run_forever).start()
    while True:
        utterance = input("Utterance: ")
        client.emit(Message(message_type='utterance', data={'text': utterance}))


if __name__ == "__main__":
    main()

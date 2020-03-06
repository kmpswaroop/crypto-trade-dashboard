import logging
import websocket
import _thread as thread


logger = logging.getLogger('websocket_provider')


class WebsocketClient(object):
    def __init__(self, url, on_message_callback=None):
        self.url = url
        self.on_message_callback = on_message_callback

    def __on_open__(self):
        logger.debug('Opened Websocket Connection')

    def __on_close__(self):
        logger.debug('Websocket connection closed')

    def __on_message__(self, message):
        logger.debug('Received Message %s', message)
        if(self.on_message_callback is not None):
            try:
                self.on_message_callback(message)
            except Exception as e:
                logger.error('Error on invoking callback', e)

    def __listen__(self):
        while self.ws.connected:
            message = self.ws.recv()
            self.__on_message__(message)
    
    def connect(self):
        self.ws = websocket.create_connection(url = self.url)
        self.__on_open__()
        thread.start_new_thread(self.__listen__, ())

    def disconnect(self):
        self.ws.close()
        self.__on_close__()
    
    def send(self, message):
        self.ws.send(message)

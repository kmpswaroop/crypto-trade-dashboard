import json
import _thread as thread
import time
from dashboard.client import WebsocketClient


class TradeDashboard(object):
    def __init__(self):
        self.trade_agg = None
        self.bid = None
        self.ask = None
        self.__start_print_thread__()

    def __update_trade_aggregate__(self, message):
        self.trade_agg = message.get('p')

    def __update_depth__(self, message):
        self.ask = message.get('a')
        self.bid = message.get('b')

    def handle_message(self, str_message):
        message = json.loads(str_message)
        event = message.get('e')
        if(event == 'aggTrade'):
            self.__update_trade_aggregate__(message)
        elif(event == 'depthUpdate'):
            self.__update_depth__(message)

    def __start_print_thread__(self):
        def run(*args):
            while True:
                self.__print_status__()
                time.sleep(1)
        thread.start_new_thread(run, ())

    def __print_status__(self):
        if(self.trade_agg is None or self.ask is None or self.bid is None):
            return
        print('Status: ')
        for b in self.bid:
            print(b[0], b[1])
        print('----------')
        print(self.trade_agg)
        print('----------')
        for a in self.ask:
            print(a[0], a[1])
        print()


def run():
    url = "wss://stream.binance.com:9443/ws/btcusdt"
    subscribe_message = {'method': 'SUBSCRIBE',
                         'params': ['btcusdt@aggTrade', 'btcusdt@depth'],
                         'id': 1}
    dashboard = TradeDashboard()
    client = WebsocketClient(url, dashboard.handle_message)
    client.connect()
    client.send(json.dumps(subscribe_message))

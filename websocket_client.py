#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import websocket
import time

class WebSocketClient:

    def __init__(self, uri):
        self.uri = uri
        self.on_opened = None
        self.on_messaged = None
        self.on_closed = None
        self.on_error = None
        self.ws = None
        self.timeout = 3

    def open(self):
        ''' WebSocketサーバに接続します '''
        self.ws = websocket.WebSocketApp(
            self.uri,
            on_message=self.on_messaged,
            on_error=self.on_error,
            on_close=self.on_closed
            )
        self.ws.on_open = self.on_opened

        # 接続処理後は別スレッドで待機
        runner = threading.Thread(target=self.__run)
        runner.setDaemon(True)
        runner.start()

        # 接続完了まで待機(タイムアウトの場合あり)
        count = self.timeout
        while not self.ws.sock.connected and count:
            time.sleep(1)
            count -= 1

    def __run(self):
        print "run"
        self.ws.run_forever()

    def send(self, message):
        ''' 文字列を送信します '''
        if not self.ws:
            raise Exception("websocket is not open.")
        self.ws.send(message)

    def close(self):
        ''' 接続を閉じます。 '''
        self.ws.close()


def message_listener(ws, message):
    print message

def closed_listener(ws):
    print "closed"

if __name__ == '__main__':
    client = WebSocketClient('ws://localhost:8080/websocket')
    client.on_messaged = message_listener
    client.on_closed = closed_listener
    client.open()
    client.send('hoge')
    while True:
        time.sleep(1)
        client.send("foo")
    client.close()

# coding: utf-8
from socketIO_client import SocketIO
import requests
from urlparse import urljoin
from functools import partial
import os


class LiveChanApi(SocketIO):
    def __init__(self, url, channel, password):
        self.url = url
        self.channel = channel
        self.password = password
        super(LiveChanApi, self).__init__(url, cookies={'password_livechan': password})
        self.emit('subscribe', channel)

    def post(self, body, name="Anonymous", convo="General", trip="", file=""):
        if trip:
            name = '{}##{}'.format(name, trip)
        data = {
            'chat': self.channel,
            'name': name,
            'trip': trip,
            'body': body,
            'convo': convo,
        }
        files = {'image': (os.path.basename(file), open(file, 'rb'))} if file else {}
        requests.post(
            urljoin(self.url, 'chat/{}'.format(self.channel)),
            data=data, files=files, cookies={'password_livechan': self.password}
        )

    def on_chat(self, callback):
        self.on('chat', partial(callback, self))

import json
import threading
import traceback

import zmq


class Subscriber:
    def __init__(self, ip, port):
        self.subscriber = ZMQSubscriber(ip, port)

    def subscribe(self, topic, callback):
        self.subscriber.subscribe(topic, callback)

    def unsubscribe(self, topic):
        self.subscriber.unsubscribe(topic)

    def stop_subscriber(self):
        self.subscriber.close_socket()


class ZMQSubscriber:

    def __init__(self, ip, port):
        self.callback = None
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.bind = 'tcp://' + ip + ':' + port
        self.is_running = True

    def subscribe(self, channel, callback):
        self.socket.connect(self.bind)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, channel)
        worker = threading.Thread(target=self.fetch_updates)
        worker.start()
        self.callback = callback

    def unsubscribe(self, channel):
        self.socket.setsockopt_string(zmq.UNSUBSCRIBE, channel)

    def fetch_updates(self):
        while self.is_running:
            try:
                message_data = self.socket.recv().decode()
                _, _, message = message_data.partition(":")
                self.callback(json.loads(message))
            except:
                print("Error: the received data contains problems.")
                traceback.print_exc()

    def close_socket(self):
        self.is_running = False
        self.socket.close()

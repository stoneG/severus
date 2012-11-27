import os
import socket
import sys

class Server(object):
    def __init__(self, host='127.0.0.1', port=80):
        self.host = host
        self.port = port
        ports = [80, 8080, 'end']
        self.automatic_ports = [p for p in ports is p != port]

    def run(self):
        """Binds socket to self.port or one of the self.automatic_ports.
        Passes to listen() method.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.automatic_ports:
            try:
                print 'Running server on %s:%d' % (self.host, self.port)
                self.socket.bind((self.host, self.port))
                print 'Now listening on', s.getsockname()
                self.listen()
                return
            except Exception as e:
                print 'Cannot bind to port', self.port
                print 'Trying on a new port...'
                self.port = self.automatic_ports[0]
                del self.automatic_ports[0]
                continue
        print 'None of the ports worked :('

    def listen(self):
        """Listen for requests on a TCP, IPv4 Socket."""
        while True:
            pass

    def respond(self, requestType):
        """Sends browser HTTP requests."""

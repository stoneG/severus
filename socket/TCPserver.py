import os
import socket
import sys

class Server(object):
    def __init__(self, host='127.0.0.1', port=80):
        self.host = host
        self.port = port
        ports = [80, 8080, 'end']
        self.automatic_ports = [p for p in ports if p != port]

    def run(self):
        """Binds socket to self.port or one of the self.automatic_ports.
        Passes to listen() method.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while self.automatic_ports:
            try:
                print 'Running server on %s:%d' % (self.host, self.port)
                self.socket.bind((self.host, self.port))
                print 'Now listening on', self.socket.getsockname()
            except Exception as e:
                print 'Cannot bind to port', self.port
                print 'Trying on a new port...'
                self.port = self.automatic_ports[0]
                del self.automatic_ports[0]
                continue
            self.listen()
            return
        print 'None of the ports worked :('

    def listen(self):
        """Listen for requests on a TCP, IPv4 Socket."""
        while True:
            print 'Waiting for connection'
            self.socket.listen(1)
            conn, addr = self.socket.accept()
            print 'Accepted connection from:', addr

            msg = conn.recv(1024)
            request = msg.split()[0]
            print 'HTTP Request:', request

            self.respond(request, conn)

    def respond(self, requestType, conn):
        """Responds to HTTP requests."""
        file_requested = string.split(' ')[1]
        print file_requested


def main():
    if len(sys.argv) == 3:
        server = Server(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        server = Server(sys.argv[1])
    else:
        server = Server()
    server.run()

if __name__ == '__main__':
    main()

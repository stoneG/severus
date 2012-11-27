import os
import socket
import sys
import time

"""
EXAMPLE OF A GET REQUEST
========================
GET / HTTP/1.1
Host: localhost:8080
Connection: keep-alive
Cache-Control: max-age=0
User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en-US,en;q=0.8
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3
Cookie: splashShown1.6=1; JSESSIONID=159lh3e376hkcvet60o8ibsq4
"""

class Server(object):
    def __init__(self, host='127.0.0.1', port=80):
        self.host = host
        self.port = port
        ports = [80, 8080, 'end']
        self.automatic_ports = [p for p in ports if p != port]
        self.www_dir = 'TCPserver'

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
            print '\nWaiting for connection'
            self.socket.listen(1)
            conn, addr = self.socket.accept()
            print 'Accepted connection from:', addr

            msg = conn.recv(1024)
            msg = msg.decode()
            request = msg.split()[0]
            print '\nHTTP Request:', request

            if request == 'GET':
                self.GET(conn, addr, msg)
            else:
                print 'Unknown HTTP request.'

    def generate_header(self, code):
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        if code == 200:
            h = 'HTTP/1.1 200 OK\n'
            h += 'Date: ' + current_date +'\n'
            h += 'Connection: close\n\n'
        elif code == 404:
            h = 'HTTP/1.1 404 Not Found\n'
            h += 'Date: ' + current_date +'\n'
            h += 'Connection: close\n\n'
        return h

    def GET(self, conn, addr, msg):
        """Responds to GET requests."""
        url_request = msg.split()[1]
        url_request = url_request.split('?')[0]
        print addr, 'is requesting', url_request

        if url_request == '/':
            url_request = '/index.html' # default to index.html
        elif url_request.split('.')[1] in ['ico']:
            print 'ignoring favicon.ico request'
            conn.close()
            return

        url_request = self.www_dir + url_request

        try:
            f = open(url_request, 'r')
            f_requested = f.read()
            f.close()
            print 'CODE: 200'
            get_request = self.generate_header(200) + f_requested
        except IOError:
            print 'CODE: 404'
            get_request = self.generate_header(404)

        get_request = get_request.encode('utf-8')
        print 'Serving GET request'
        conn.send(get_request)
        print 'Closing connection'
        conn.close()

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

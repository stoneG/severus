import os
import socket
import sys
import pdb
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

EXAMPLE OF A POST REQUEST
=========================
POST / HTTP/1.1
TE: deflate,gzip;q=0.3
Connection: TE, close
Host: 127.0.0.1:13373
User-Agent: lwp-request/6.03 libwww-perl/6.03
Content-Length: 57
Content-Type: application/x-www-form-urlencoded

[POST TEXT]

"""
class Page(object):
    def __init__(self):
        self.img_exts = ['ico', 'png', 'jpg', 'jpeg', 'gif']
        self.content_type = ['application/x-www-form-urlencoded', 'application/json']


class Server(object):
    def __init__(self, host='127.0.0.1', port=80):
        self.host = host
        self.port = port
        ports = [80, 8080, 'end']
        self.automatic_ports = [p for p in ports if p != port]
        self.www_dir = 'TCPserver'
        self.page = Page()

    def run(self):
        """Binds socket to self.port or one of the self.automatic_ports.
        Passes to listen() method.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        self.socket.listen(3)
        while True:
            print '\nWaiting for connection'
            conn, addr = self.socket.accept()
            pid = os.fork()
            if pid == 0:
                print 'Accepted connection from:', addr

                msg = conn.recv(1024)
                msg = msg.decode()
                request = msg.split()[0]
                print '\nHTTP Request:', request

                if request == 'GET' or request == 'HEAD':
                    self.GET(conn, addr, msg)
                elif request == 'POST':
                    self.POST(conn, addr, msg)
                else:
                    print 'Unknown HTTP request.'
                os._exit(0)
            else:
                conn.close()
                continue

    def generate_header(self, code):
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        if code == 200:
            h = 'HTTP/1.1 200 OK\n'
        elif code == 404:
            h = 'HTTP/1.1 404 Not Found\n'
        h += 'Date: ' + current_date +'\n'
        h += 'Connection: close\n\n'
        return h

    def parse_url(self, msg, addr):
        """Given a HTTP request, return the parsed url."""
        url_request = msg.split()[1]
        url_request = url_request.split('?')[0]
        print addr, 'is requesting', url_request

        if url_request == '/':
            url_request = '/index.html' # default to index.html

        url_request = self.www_dir + url_request
        return url_request

    def GET(self, conn, addr, msg):
        """Responds to GET requests."""
        url_request = self.parse_url(msg, addr)
        try:
            f = open(url_request, 'r')
            f_requested = f.read()
            f.close()
            print 'CODE: 200'
            get_request = self.generate_header(200) + f_requested
        except IOError:
            print 'CODE: 404'
            f = open(self.www_dir+'/fourohfour.html', 'r')
            f_requested = f.read()
            get_request = self.generate_header(404) + f_requested

        if url_request.split('.')[1] not in self.page.img_exts:
            get_request = get_request.encode('utf-8')
        print 'Serving request'
        conn.send(get_request)
        print 'Closing connection'
        conn.close()

    def _POST_url(self, baseUrl, msg):
        if 'eggs' in msg:
            if 'eggs=scrambled' == msg:
                requested_file = baseUrl + '?' + msg
            else:
                requested_file = baseUrl + '?eggs=else'
        return requested_file

    def POST(self, conn, addr, msg):
        """Prints POST request data to console."""
        url_request = self.parse_url(msg, addr)
        header = msg.split('\r\n\r\n')[0]
        for content_type in self.page.content_type:
            if content_type in header:
                post_type = content_type
                message = msg.replace(header,'')[4:]
                print 'POST Content_Type:', post_type
                print message
                print 'CODE: 200'
                f = open(self._POST_url(url_request, message), 'r')
                f_requested = f.read()
                f.close()
                post_request = self.generate_header(200) + f_requested
                conn.send(post_request)
                conn.close()
                return
        print 'POST Content_Type not recognized'
        print message
        print 'CODE: 404'
        post_request = self.generate_header(404)
        conn.send(post_request)
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

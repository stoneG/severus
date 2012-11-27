import string
import cgi
import time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith(".html"):
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            if self.path.endswith(".esp"): # our dynamic content
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                msg = "hey, today is the " + str(time.localtime()[7])
                self.wfile.write(msg)
                msg = " day in the year " + str(time.localtime()[0])
                self.wfile.write(msg)
                return
            return
        except IOError:
            self.send_error(404, 'OMG File Not Found: %s' % self.path)

def main():
    try:
        server = HTTPServer(('', 5000), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

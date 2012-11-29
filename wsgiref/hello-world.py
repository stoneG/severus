from urlparse import parse_qs
from cgi import escape
from wsgiref.simple_server import make_server
import os
import pdb

def hello_world(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'subject' in parameters:
        subject = escape(parameters['subject'][0]) # escapes $, <, > to html-safe
    else:
        subject = 'World'
    start_response('200 OK', [('Content-Type', 'text/html')])
    return ['Hello {0}s'.format(subject)]

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8080, hello_world)
    server.serve_forever()

# localhost:8080/?subject=Sitong

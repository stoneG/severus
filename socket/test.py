import os
import sys
import time

# python test.py 127.0.0.1 8080 '/index.html'
host = sys.argv[1] if len(sys.argv) == 4 else '127.0.0.1'
port = sys.argv[2] if len(sys.argv) == 4 else 8080
url = sys.argv[3] if len(sys.argv) == 4 else ''

print 'now blasting the TCP server with 20 HEAD requests'

counter = 20
t = time.time()*1000
while counter:
    os.system('HEAD %s:%d%s' % (host, port, url))
    counter -= 1
print '20 HEAD requests took %d milliseconds' % (time.time()*1000 - t)

import socket

host = '127.0.0.1'
port = 13373

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(1)
print 'listening on', host, port

while True:
    conn, addr = s.accept()
    message = conn.recv(1024)
    print 'Message received from %s' % str(addr)
    print repr(message)

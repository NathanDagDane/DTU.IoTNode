import network
import socket
import ujson
from pins import pins

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'Tony')
ap.config (authmode = 3, password = '12345687')

html_path = '/index.html'
with open(html_path, 'r') as f:
    html = f.read()

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    request_line = cl_file.readline()
    print("Request:", request_line)
    method, path, _ = request_line.decode().split()
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    if path == '/data': # Endpoint for JSON data
        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
        data = [{'name': n, 'pin': p.name, 'value': p.value()} for n, p in pins.items()]
        cl.send(ujson.dumps(data))
    else: # Default endpoint for HTML
        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(html)

    cl.close()

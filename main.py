import network
import socket
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
    while True:
        line = cl_file.readline()
        #print(line)
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (n, p.name, p.value()) for n,p in pins.items()]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()

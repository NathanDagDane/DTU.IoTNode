import network
import socket
import ujson
import random
from machine import Pin
from pins import pins

def handle_button(pin):
    pins['LED-Green'].set(random.uniform(0, 1))
    pins['LED-Orange'].set(random.uniform(0, 1))
    pins['LED-Red'].set(random.uniform(0, 1))

pins['Button'].pin.irq(trigger=Pin.IRQ_RISING, handler=handle_button)

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
    _, path, _ = request_line.decode().split()

    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break

    if path[:5] == "/data": # Request for data
        path = path[6:]
        if path == '': # Request for all data
            cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
            data = [{'name': n, 'pin': p.name, 'value': p.value()} for n, p in pins.items()]
            cl.send(ujson.dumps(data))
        else: # Request for specific data
            cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n")
            print(path[:-1])
            data = [{'name': n, 'pin': p.name, 'value': p.value()} for n, p in filter(lambda x: x[1].type == path[:-1], pins.items())]
            cl.send(ujson.dumps(data))
    elif path[:4] == "/set": # Request to set a pin value
            path = path[5:]
            device, value = path.split('/')
            if device in pins:
                pins[device].set(float(value))
                cl.send(b"HTTP/1.0 200 OK\r\n\r\n")
            else:
                cl.send(b"HTTP/1.0 404 NO SUCH DEVICE\r\n\r\n")
    elif '.' in path: # Request for a file
        try:
            with open(path, 'r') as f:
                cl.send(f.read())
        except:
            cl.send(b"HTTP/1.0 404 NO SUCH FILE\r\n\r\n")
    else: # Default endpoint for HTML
        cl.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(html)

    cl.close()

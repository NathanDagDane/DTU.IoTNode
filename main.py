from machine import Pin, ADC
import network
import socket

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'Tony')
ap.config (authmode = 3, password = '12345687')

p36 = ADC(Pin(36), atten=ADC.ATTN_11DB)
p36.width(ADC.WIDTH_12BIT)
pins = [p36]

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
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.read()) for p in pins]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()

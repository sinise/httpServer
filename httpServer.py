import sys
import gevent
from gevent import socket
from email.Utils import formatdate

def handle_socket(sock):

    #handling the request
#    print 'handle socket start'
    fileNotFound = False
    data = sock.recv(4096)
    data2 = ''
    count = 0
    while True:
       
        data2 = data2 + data
        if (data2[-4:] == '\r\n\r\n') or count > 10:
            break
        data = sock.recv(4096)
	count = count + 1
    print data2
    request = data2.split("\r\n")
    requestLine = request[0].split(' ')
    type = requestLine[0]
    path = requestLine[1]
    #if no path is given set path to index.html
    if path == "/":
        path = "/index.html"
    #open requested file
    try:
        file = open(serverPath + path, "rb")
    except:
        fileNotFound = True

    #If file was not found
    if fileNotFound:
        sock.sendall("HTTP/1.1 404 Not Found\r\n")
        sock.sendall("Connection: Close\r\n")
        sock.close()

    #File was found send headers and content
    else:
        sock.sendall("HTTP/1.1 200 OK\r\n")
        sock.sendall("Date: " +  formatdate() + "GMT\r\n")
        sock.sendall("Connection: Close\r\n\r\n")
        fi = file.read(1024)
        while (fi):
            sock.sendall(fi)
            fi = file.read(1024)
        sock.close()

if not (len(sys.argv) == 4):
    print 'Usage: "python httpServer.py <path> <address> <port>\n'
    sys.exit(2)

serverPath = sys.argv[1]
ip = sys.argv[2]
port = int(sys.argv[3])

#    out.write(received[1])
#    out.close()


server = socket.socket()
server.bind((ip, port))
server.listen(500)

while True:
    try:
        new_sock, address = server.accept()
    except KeyboardInterrupt:
        break
    # handle every new connection with a new coroutine
    gevent.spawn(handle_socket, new_sock)



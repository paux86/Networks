import socket, logging

def client():
    port = 9001
    host = '127.0.0.1'

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    sock.setblocking(True)
    logging.info('Connect to server: ' + host + ' on port: ' + str(port))

    #request = b'GET /hello.html HTTP/1.1\r\nHost: localhost:9001\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:69.0) Gecko/20100101 Firefox/69.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nCache-Control: max-age=0\r\n\r\nname=Matt&course=Comp429'
    #request = b'HEAD /hello.html HTTP/1.1\r\nHost: localhost:9001\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:69.0) Gecko/20100101 Firefox/69.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nCache-Control: max-age=0\r\n\r\nname=Matt&course=Comp429'
    request = b'POST /hello.html HTTP/1.1\r\nHost: localhost:9001\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:69.0) Gecko/20100101 Firefox/69.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nCache-Control: max-age=0\r\n\r\nname=Matt&course=Comp429'

    sock.send(request)

    response = sock.recv(1024)
    print(response.decode('utf-8'))

    sock.close()

client()
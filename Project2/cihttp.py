# Matt Brierley
# Comp 429, Project 2

import socket, logging, threading
import json, os, time, datetime

# Comment out the line below to not print the INFO messages
logging.basicConfig(level=logging.INFO)


class HttpRequest():
    def __init__(self, requeststr):
        self.rstr = requeststr
        self.rjson = {}
        self.parse_string()


    def parse_string(self):
        req = self.rstr.splitlines()

        # request line
        request_line = req[0].split()
        req_data = {}
        req_data['request_line'] = {}
        req_data['request_line']['method'] = request_line[0]
        req_data['request_line']['URI'] = request_line[1]
        req_data['request_line']['version'] = request_line[2]

        # headers
        req_data['headers'] = []
        for line in req[1:]:
            split = line.split(': ')

            if not line:
                break

            req_data['headers'].append({ split[0] : split[1] })

        # body
        req_data['body'] = ''
        if len(req) > len(req_data['headers']) + 2:
            req_data['body'] = req[-1]


        self.rjson = json.dumps(req_data)


    def display_request(self):
        print(self.rjson)



class ClientThread(threading.Thread):
    def __init__(self, address, socket):
        threading.Thread.__init__(self)
        self.csock = socket
        logging.info('New connection added.')


    def run(self):
        # exchange messages
        request = self.csock.recv(1024)
        req = request.decode('utf-8')
        logging.info('Recieved a request from client: ' + req)

        httpreq = HttpRequest(req)

        httpreq.display_request()

        # handle request
        response = ''

        response_data = json.loads(httpreq.rjson)
        method = response_data['request_line']['method']

        if method in ['HEAD', 'GET']:
            try:
                path = 'www' + response_data['request_line']['URI']
                f = open(path, "r")
                
                size = os.path.getsize(path)

                modTimeSinceEpoch = os.path.getmtime(path)
                modificationTime = datetime.datetime.utcfromtimestamp(modTimeSinceEpoch).strftime('%a, %d %b %Y %H:%M:%S GMT')

                response = "HTTP/1.1 200 OK\r\nContent-Length: " + str(size) + "\r\nServer: cihttpd\r\nLast-Modified: " + modificationTime + "\r\n\r\n"

                if method == 'GET':
                    response = response + f.read()
            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\nServer: cihttpd\r\n\r\n<html><body><h1>404 File Not Found</h1></body></html>"
        elif method == 'POST':
            data_entered = response_data['body']
            data_entered = data_entered.replace('=', ': ')
            data_entered = data_entered.replace('&', '<br />')
            responseHTML = "<html><body><h1>Post</h1><p>" + data_entered + "</p></body></html>"

            utcTime = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

            size = len(responseHTML.encode('utf-8'))

            response = "HTTP/1.1 200 OK\r\nContent-Length: " + str(size) + "\r\nServer: cihttpd\r\nLast-Modified: " + utcTime + "\r\n\r\n" + responseHTML
        else:
            # invalid method
            pass
        
        # send a response
        self.csock.send(response.encode('utf-8'))

        # disconnect client
        self.csock.close()
        logging.info('Disconnect client.')


def server():
    logging.info('Starting cihttpd...')

    # start serving (listening for clients)
    port = 9001
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost',port))

    while True:
        sock.listen(1)
        logging.info('Server is listening on port ' + str(port))

        # client has connected
        sc,sockname = sock.accept()
        logging.info('Accepted connection.')
        t = ClientThread(sockname, sc)
        t.start()


server()


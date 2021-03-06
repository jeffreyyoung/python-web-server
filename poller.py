import errno
import select
import socket
import sys
import traceback
import time
from http_request_parser import ParsedHttpRequest
from config_file_parser import ParsedConfigFile
from http_response import HttpResponseBuilder

class Poller:
    """ Polling server """
    def __init__(self,port):
        self.config = ParsedConfigFile()
        self.host = ""
        self.port = port
        self.open_socket()
        self.clients = {}
        self.timeouts = {}
        self.cache = {}
        self.size = 1024
        self.responseBuilder = HttpResponseBuilder(self.config)

    def open_socket(self):
        """ Setup the socket for incoming clients """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
            self.server.setblocking(0)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)
    def sweepClients(self):
        for key in self.timeouts.keys():
            if (time.time() - self.timeouts[key]) > self.timeout:
                print "delete client: " + str(key)
                #self.clients[fd].close()
                del self.timeouts[key]
                del self.clients[key]

    def run(self):
        """ Use poll() to handle each incoming client."""
        self.poller = select.epoll()
        self.pollmask = select.EPOLLIN | select.EPOLLHUP | select.EPOLLERR
        self.poller.register(self.server,self.pollmask)
        self.timeout = float(self.config.parameters["timeout"])
        lastSweep = time.time()

        while True:

            if (time.time() - lastSweep) > self.timeout:
                #kill all client older than time
                self.sweepClients()
                lastSweep = time.time()
            # poll sockets
            try:
                fds = self.poller.poll(timeout=1)
            except:
                return
            for (fd,event) in fds:
                # handle errors
                if event & (select.POLLHUP | select.POLLERR):
                    self.handleError(fd)
                    continue
                # handle the server socket
                if fd == self.server.fileno():
                    self.handleServer()
                    continue
                # handle client socket
                result = self.handleClient(fd)

    def handleError(self,fd):
        self.poller.unregister(fd)
        if fd == self.server.fileno():
            # recreate server socket
            self.server.close()
            self.open_socket()
            self.poller.register(self.server,self.pollmask)
        else:
            # close the socket
            self.clients[fd].close()
            del self.clients[fd]
            del self.timeouts[fd]

    def handleServer(self):
        # accept as many clients are possible
        while True:
            try:
                (client,address) = self.server.accept()
            except socket.error, (value,message):
                # if socket blocks because no clients are available,
                # then return
                if value == errno.EAGAIN or errno.EWOULDBLOCK:
                    return
                print traceback.format_exc()
                sys.exit()
            # set client socket to be non blocking
            client.setblocking(0)
            self.clients[client.fileno()] = client
            self.timeouts[client.fileno()] = time.time()
            self.poller.register(client.fileno(),self.pollmask)

    def handleClient(self,fd):
        try:
            data = self.clients[fd].recv(self.size)
            self.timeouts[fd] = time.time()
        except socket.error, (value,message):
            # if no data is available, move on to another client
            if value == errno.EAGAIN or errno.EWOULDBLOCK:
                return
            print traceback.format_exc()
            sys.exit()
        if data:
            if "\r\n\r\n" in data:
                if fd in self.cache:
                    data = self.cache[fd] + data
                    del self.cache[fd]

                request = ParsedHttpRequest(data)
                res = self.responseBuilder.getResponse(request)
                self.clients[fd].send(res)
                self.timeouts[fd] = time.time()
            else:
                if not fd in self.cache:
                    self.cache[fd] = data
                else:
                    self.cache[fd] += data

        else:
            self.poller.unregister(fd)
            self.clients[fd].close()
            del self.clients[fd]
            del self.timeouts[fd]
            if fd in self.cache:
                del self.cache[fd]


# str = "123456789abcdefghijklmnopqrstuvwyz"
# print str[0:4]
# print str[4:8]
# print str[8:11]
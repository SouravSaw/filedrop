#! /usr/bin/python

import socket
from time import sleep
import threading

discoveredNodes = {}


def handleBroadcast(address, message):
    discoveredNodes[address] = str(message)
    print discoveredNodes


class udpBroadcasterThread(threading.Thread):
    """broadcast UDP sockets (process runs in a separate thread of control)"""
    def __init__(self, PORT, address='<broadcast>', threadName=None):
        threading.Thread.__init__(self)
        self.name = threadName
        self.PORT = PORT
        self.address = address

    exitFlag = 0

    def run(self):
        broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while(self.exitFlag == 0):
            broadcastSocket.sendto('Broadcast message!',
                                   (self.address, self.PORT))
            #print "broadcasting \n"
            sleep(2)

    def startBroadcast(self):
        self.start()

    def stopBroadcast(self):
        self.exitFlag = 1


class udpBroadcaster(object):

    """broadcast UDP packets"""

    def __init__(self, PORT, address='<broadcast>'):
        self.address = address
        self.PORT = PORT

    def start(self):
        broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            broadcastSocket.sendto('Broadcast message!',
                                   (self.address, self.PORT))
            #print "broadcasting \n"
            sleep(2)


class udpListnerThread(threading.Thread):
    """listen UDP broadcasts (process runs in a separate thread of control)"""
    def __init__(self, PORT, address='', threadName=None):
        threading.Thread.__init__(self)
        self.name = threadName
        self.PORT = PORT
        self.address = address

    exitFlag = 0

    def run(self):
        listnerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listnerSocket.bind((self.address, self.PORT))
        while(self.exitFlag == 0):
            data, address = listnerSocket.recvfrom(1024)
            #print 'The client at', address, 'says', repr(data)
        #listnerSocket.sendto('Your data was %d bytes' % len(data), address)
            handleBroadcast(address, data)

    def startListner(self):
        self.start()

    def stopListner(self):
        self.exitFlag = 1


class udpListner(object):
    """listen UDP broadcasts"""
    def __init__(self, PORT, address=''):
        self.PORT = PORT
        self.address = address

    def start(self):
        listnerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listnerSocket.bind((self.address, self.PORT))
        while True:
            data, address = listnerSocket.recvfrom(1024)
            print 'The client at', address, 'says', repr(data)
#listnerSocket.sendto('Your data was %d bytes' % len(data), address)
            handleBroadcast(address, data)

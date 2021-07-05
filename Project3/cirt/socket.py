# Matt Brierley

import socket
from .packet import Packet
from .common import *
from .controlblock import ControlBlock
from .coutput import Coutput
from .cinput import Cinput
import logging

class Socket:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.cb = ControlBlock()
        self.cb.sock = sock
        self.coutput = Coutput(self.cb)
        self.cinput = Cinput(self.cb)
        

    ##################################################################
    # API Calls - used by the client and server.
    # All your hard work is hidden by these few functions.
    # Let's take a moment to thank everyone who has worked on
    # implementing TCP for our respective operating systems.
    ##################################################################
    def connect(self, address):
        self.cb.dst = address

        # send syn
        self.coutput.cirt_output()
        self.cb.state = SYN_SENT

        # wait for syn + ack
        packet, addr = self.cinput.cirt_input()
        if packet.is_synack() and packet.ackno == (self.cb.seqno + 1):
            self.cb.state = ESTABLISHED

            # send ack
            self.cb.seqno += 1
            self.cb.ackno = (packet.seqno + 1)
            self.coutput.cirt_output()


    def listen(self, port):
        addr = ('127.0.0.1', port)
        self.cb.sock.bind(addr)
        self.cb.state = LISTEN


    def accept(self):
        print("accept a connection!")
        
        while True:
            self.cb.seqno = S_ISN
            # wait for syn packet, parse
            packet, addr = self.cinput.cirt_input()
            self.cb.dst = addr
            if packet.is_syn():
                self.cb.state = SYN_RECV

                # build and send syn + ack packet
                self.cb.ackno = (packet.seqno + 1)
                self.coutput.cirt_output()

                # wait for ack packet, parse
                packet, addr = self.cinput.cirt_input()
                if packet.is_ack() and packet.ackno == (self.cb.seqno + 1):
                    self.cb.state = ESTABLISHED

                break


    def send(self, data):
        print("send some data!")

        # build and send data packet
        self.cb.snd_buf = data
        self.coutput.cirt_output()

        # wait for ack
        packet, addr = self.cinput.cirt_input()
        if packet.is_ack():
            self.cb.seqno = packet.ackno


    def recv(self, size):
        print("receive some data!")

        # receive and parse data packet
        packet, addr = self.cinput.cirt_input()

        if packet.is_fin():
            self.cb.state = CLOSE_WAIT
            self.cb.ackno = (packet.seqno + 1)
        else:
            self.cb.ackno = (packet.seqno + len(packet.data))

        # send ack
        self.coutput.cirt_output()

        return packet.data



    def close(self):
        print("we done here")

        if self.cb.state == ESTABLISHED:
            self.cb.state = FIN_WAIT_1
        elif self.cb.state == CLOSE_WAIT:
            self.cb.state = LAST_ACK
        
        # build and send fin + ack packet
        self.cb.snd_buf = b''
        self.coutput.cirt_output()

        # wait for ack
        packet, addr = self.cinput.cirt_input()
        if packet.is_ack():
            if self.cb.state == LAST_ACK:
                self.cb.state = CLOSED
            elif self.cb.state == FIN_WAIT_1:
                self.cb.state = FIN_WAIT_2
        
        if self.cb.state == FIN_WAIT_2:
            # wait for fin
            packet, addr = self.cinput.cirt_input()
            if packet.is_fin():
                self.cb.state = TIME_WAIT
                self.cb.ackno = (packet.seqno + 1)
                self.coutput.cirt_output()
        
        self.cb.sock.close()


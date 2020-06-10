# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# Mold UDP packet encoder according to the specification from Nasdaq
#
from struct import *

from mold_const import *


# MoldUDP (http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/moldudp64.pdf)
class MoldUDPEncoder:

    # publisher is the message sender to the wire
    def __init__(self, publisher, debug=False):
        self._offset = SESSION_OFFSET
        self._publisher = publisher
        self._debug = debug
        self._msgblks = []
        self._header = bytearray(HEADER_SIZE)
        self._buffer = bytearray(PAYLOAD_SIZE)
        self._packet = bytearray(MOLDPKT_SIZE)
        self._left = PAYLOAD_SIZE
        self._seq = 0
        self._msgcount = 0

    def _encode(self):
        if (self._publisher == None):
            return

        published = False
        # clear payload buffers
        self._header[:] = b'\x00' * HEADER_SIZE
        self._buffer[:] = b'\x00' * PAYLOAD_SIZE

        if (self._debug == True):
            print("SEND HDR SESSION: {}".format(self._session))
            print("SEND HDR SEQ:     {}".format(self._seq))

        # encode payload until it can't fit
        self._offset = 0
        remaining = PAYLOAD_SIZE
        while (len(self._msgblks) > 0):
            # pop the message block from the beginning of queue
            msg = self._msgblks.pop(0)
            sz = len(msg)
            if ((self._offset + MESSAGE_SIZE_FIELD_LEN + sz) < remaining):
                #print("PRE MSG SIZE OFFSET: {}".format(self._offset))
                pack_into('>H', self._buffer, self._offset, sz)
                self._offset += MESSAGE_SIZE_FIELD_LEN
                #print("POST MSG SIZE OFFSET: {}".format(self._offset))
                fmt = ">{}s".format(sz)
                pack_into(fmt, self._buffer, self._offset, msg)
                self._offset += sz
                #print("MSG DATA OFFSET: {}".format(self._offset))
                self._msgcount += 1
                published = False
            else:
                # can't fit into the buffer going out so
                # put the message block back to the front of queue
                self._msgblks.insert(0, msg)
                # payload is filled, now update header with latest count and send
                self._send()
                published = True
                break
        # Flushing the last packet even it didn't fill up the buffer
        if ((published == False) and (self._offset < remaining)):
            # now update header with latest count and send
            self._send()
            published = True

    def _send(self):
        pack_into('>10sQh', self._header, 0, self._session, self._seq, self._msgcount)
        if (self._debug == True):
            print("SEND MSG COUNT:   {}".format(self._msgcount))
            print("SEND HDR: {}".format(self._header))
        # combine header and payload to create mold packet
        self._packet[:PAYLOAD_OFFSET] = self._header
        self._packet[PAYLOAD_OFFSET:] = self._buffer
        self._publisher.publish(self._packet)
        self._seq += self._msgcount
        self._offset = 0
        self._msgcount = 0

    def session(self, session):
        self._session = session

    def seq(self, seq):
        self._seq = seq

    def msgcount(self):
        return len(self._msgblks)

    def add_msg(self, msg):
        if (msg == None):
            return
        self._msgblks.append(msg)
        self._left -= len(msg)
        # force encode if buffer is filled
        if (self._left < (MESSAGE_SIZE_FIELD_LEN + 1)):
            self._encode()
            self._left = PAYLOAD_SIZE

    def process(self):
        while (self.msgcount() > 0):
            self._encode()
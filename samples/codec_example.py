# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# Sample application on how to use MoldUDP codec
# To run: python3 codec_example.py
#
from moldudp.msg.msgsub import *
from moldudp.msg.msgpub import *
from moldudp.codec.decoder import *
from moldudp.codec.encoder import *


class MoldSubscriber(MsgSubscriber):

    def __init__(self):
        # Setup a decoder to process encoded bytearray/packet
        self.__molddecoder = MoldUDPDecoder(self, True)

    def get_decoder(self):
        return self.__molddecoder

    def on_hb(self):
        print("Got heart beat")

    def on_eos(self):
        print("Got end of session")

    def on_msgblk(self, msg):
        print("RECEIVED MSG: {}".format(msg))


class MoldPublisher(MsgPublisher):

    def __init__(self, moldsub):
        self.__moldencoder = MoldUDPEncoder(self, True)
        self.__moldsub = moldsub

    def session(self, sid):
        self.__moldencoder.session(sid)

    def seq(self, seq):
        self.__moldencoder.seq(seq)

    def add_msg(self, msg):
        self.__moldencoder.add_msg(msg)

    def process(self):
        self.__moldencoder.process()

    def publish(self, msg):
        print("SENT PKT: {}".format(msg))
        # In real world, publish() writes the msg to a file or network (UDP/IP).
        # Then the subscriber reads the msg from a file or network, and
        # passes the encoded bytearray/packet to decoder to process.
        self.__moldsub.get_decoder().buffer(msg)
        self.__moldsub.get_decoder().decode()


idx = 0
cnt = 1000
moldsub = MoldSubscriber()
moldpub = MoldPublisher(moldsub)
moldpub.session(b"20200609AA")
moldpub.seq(1)
# Keep adding message block to the encoder, it sends the buffer when
# it is filled or when the last message block can not fit into the
# buffer anymore
while (idx < cnt):
    moldpub.add_msg(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    idx += 1
    moldpub.add_msg(b"CDEFGHIJKLMNOPQRSTUVWXYZAB")
    idx += 1
    moldpub.add_msg(b"EFGHIJKLMNOPQRSTUVWXYZABCD")
    idx += 1
    moldpub.add_msg(b"GHIJKLMNOPQRSTUVWXYZABCDEF")
    idx += 1

# Process the rest of the message blocks in queue
moldpub.process()

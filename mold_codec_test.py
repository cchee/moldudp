# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# Sample application on how to use MoldUDP codec
#
from mold_decoder import MoldUDPDecoder
from mold_encoder import MoldUDPEncoder
from msg_pub import MsgPublisher
from msg_sub import MsgSubscriber


class MoldDecoderTest(MsgSubscriber):

    def on_hb(self):
        print("Got heart beat")

    def on_eos(self):
        print("Got end of session")

    def on_msgblk(self, msg):
        print("RECEIVED MSG: {}".format(msg))


class MoldEncoderTest(MsgPublisher):

    def __init__(self):
        self._moldsub = MoldDecoderTest()
        self._molddeco = MoldUDPDecoder(self._moldsub, True)

    def publish(self, msg):
        print("SENT PKT: {}".format(msg))
        self._molddeco.buffer(msg)
        self._molddeco.decode()


idx = 0
cnt = 1000
moldpub = MoldEncoderTest()
moldencoder = MoldUDPEncoder(moldpub, True)
moldencoder.session(b"20200609AA")
moldencoder.seq(1)
while (idx < cnt):
    moldencoder.add_msg(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    idx += 1
    moldencoder.add_msg(b"CDEFGHIJKLMNOPQRSTUVWXYZAB")
    idx += 1
    moldencoder.add_msg(b"EFGHIJKLMNOPQRSTUVWXYZABCD")
    idx += 1
    moldencoder.add_msg(b"GHIJKLMNOPQRSTUVWXYZABCDEF")
    idx += 1

moldencoder.process()

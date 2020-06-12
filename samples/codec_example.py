# Copyright 2020 All right reserved
# Author: Chester Chee <chester.chee@gmail.com>
#
# Sample application on how to use MoldUDP codec
#
import codec.const
import codec.decoder
import codec.encoder
import codec.msgpub
import codec.msgsub


class MoldSubscriber(MsgSubscriber):

    def __init__(self):
        # Setup a decoder to process encoded bytearray/packet
        self._molddecoder = MoldUDPDecoder(self, True)

    def get_decoder(self):
        return self._molddecoder

    def on_hb(self):
        print("Got heart beat")

    def on_eos(self):
        print("Got end of session")

    def on_msgblk(self, msg):
        print("RECEIVED MSG: {}".format(msg))


class MoldPublisher(MsgPublisher):

    def __init__(self, moldsub):
        self._moldencoder = MoldUDPEncoder(self, True)
        self._moldsub = moldsub

    def session(self, sid):
        self._moldencoder.session(sid)

    def seq(self, seq):
        self._moldencoder.seq(seq)

    def publish(self, msg):
        print("SENT PKT: {}".format(msg))
        # In real world, publish() is call and then sends the msg
        # to file or network. Then ths subscriber read the msg
        # from file or network, and pass the encoded bytearray/packet
        # to decoder to process.
        self._moldsub.get_decoder().buffer(msg)
        self._moldsub.get_decoder().decode()


idx = 0
cnt = 1000
moldsub = MoldSubscriber()
moldpub = MoldPublisher(moldsub)
moldpub.session(b"20200609AA")
moldpub.seq(1)
# Keep adding message block to the encoder, it sends
# the buffer when it is filled or the last message block
# can not be added into the buffer anymore
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

#!/usr/bin/env python
# -*- coding: utf8 -*-
"""

Copyright © 2009 William Pitcock <nenolod@dereferenced.org>.

All rights reserved.  Redistribution, usage and modification are allowed, provided
that the source code to any modified versions is made available, and this copyright
notice and this permission notice are left intact.

By using this code, you acknowledge that no warranty is offered for any particular
suitability or fitness.

"""

import asyncore, socket

class ircconn(asyncore.dispatcher):
    """
    The penis.ircsocket class is used to connect to a remote IRC daemon, either
    as a server, or as a client.

    It subclasses asyncore.dispatcher for the sake of the canned event loop.
    """
    def __init__(self, hostname, port, name=None, password=None, protocol_handler=None, channels={}, friendlyname=None):
        """
        Constructor for penis.ircsocket.ircconn.

        hostname: The hostname to connect to.
        port: The port to connect to.
        password: The linking password.
        protocol_handler: The protocol handler class to use.
        """
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((hostname, port))
        self.hostname = hostname
        self.port = port
        self.name = name
        self.password = password
        self.protocol_handler = protocol_handler(self)
        self.sendq = ""
        self.readbuf = ""

        if friendlyname == None:
            friendlyname = self.hostname
        self.friendlyname = friendlyname

        self.channels = channels

        # build a dictionary of the inverse mapping.
        self.vchans = {}
        for vchan in self.channels:
             self.vchans[self.channels[vchan]] = vchan

    # sendq
    def writable(self):
        return (len(self.sendq) > 0)

    def handle_write(self):
        sent = self.send(self.sendq)
        self.sendq = self.sendq[sent:]

    def handle_read(self):
        try:
            self.readbuf += self.recv(1)
            while self.readbuf[len(self.readbuf) - 1] != '\n':
                self.readbuf += self.recv(1)

            info = self.protocol_handler.parse(self.readbuf)
            print "[%s] -> %s" % (self.hostname, info)
            self.readbuf = ""
            self.protocol_handler.handle_command_tuple(info)
        except socket.error:
            pass

    def write(self, data):
        self.sendq += data

    def write_line(self, data):
        print "[%s] <- %s" % (self.hostname, self.protocol_handler.parse(data))
        self.sendq += data + "\r\n"

    def handle_connect(self):
        self.protocol_handler.handshake(self.name, self.password)

    def handle_close(self):
        self.close()


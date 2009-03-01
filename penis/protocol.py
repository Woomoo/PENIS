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

class protocol_base(object):
    def __init__(self, socket):
        self.sock = socket

    def handshake(self, name, password):
        pass

    def parse(self, line):
        """RFC1459 parser."""
        try:
            message = line.split('\r\n')[0]
        except:
            message = line.split('\n')[0]
        info = {}

        # check for an origin, and extract it.
        if message[0] == ':':
            length = message[1:].find(' ') + 1
            info['origin'] = message[1:length]
            message = message[length + 1:]

        # next the command or numeric
        length = message.find(' ')
        info['command'] = message[:length]
        message = message[length + 1:]

        # now args
        words = []
        while message != '':
            # check for multiword
            length = message.find(' ')
            if message[0] == ':':
                words.append(message[1:])
                message = ''
            elif length != -1 and length != 0:
                words.append(message[:length])
                message = message[length + 1:]
            else:
                words.append(message)
                message = ''

        info['args'] = words
        return info

    def handle_command_tuple(self, tuple):
        try:
            self.handlers[tuple['command']](self, tuple)
        except KeyError:
            print "!!! Handler for %s not implemented" % tuple['command']

class rfc1459_client(protocol_base):
    def __init__(self, sock):
        super(rfc1459_client, self).__init__(sock)
        self.handlers = {
            'PING': self.handle_pong
        }

    def handshake(self, name, password):
        if password != None:
            self.sock.write_line("PASS %s" % password)

        self.sock.write_line("NICK %s" % name)
        self.sock.write_line("USER %s penis penis :Python External Network Integration Service" % (name))

    def handle_pong(self, tuple):
        self.sock.write_line("PONG %s" % tuple['args'][0])

if __name__ == '__main__':
    p = protocol_base(None)
    print p.parse(":lol!lol@lol PRIVMSG #lol :lol test\r\n");
    print p.parse(":irc.lol.com 001 lol :Welcome to IRC lol\r\n");
    print p.parse("002 lol moocows\r\n");


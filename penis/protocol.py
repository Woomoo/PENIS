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

clientlist = []

class protocol_base(object):
    def __init__(self, socket):
        global clientlist
        self.sock = socket
        clientlist.append(self)

    def __del__(self):
        global clientlist
        clientlist.remove(self)

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
            self.handlers[tuple['command']](tuple)
        except KeyError:
            print "!!! Handler for %s not implemented" % tuple['command']

    # action stubs
    def join_channel(self, channel):
        print "!!! join_channel stub!"

    def send_to_channel(self, channel, message):
        print "!!! send_to_channel stub!"

    # event stubs
    def handle_channel_message(self, info):
        print "!!! handle_channel_message stub!"

class rfc1459_client(protocol_base):
    def __init__(self, sock):
        super(rfc1459_client, self).__init__(sock)
        self.handlers = {
	    '001': self.handle_001,
            'PING': self.handle_pong,
            'PRIVMSG': self.handle_privmsg
        }

    def handshake(self, name, password):
        if password != None:
            self.sock.write_line("PASS %s" % password)

        self.sock.write_line("NICK %s" % name)
        self.sock.write_line("USER %s penis penis :Python External Network Integration Service" % (name))

    def handle_001(self, tuple):
        for vchan in self.sock.channels:
             self.join_channel(self.sock.channels[vchan])

    def handle_pong(self, tuple):
        self.sock.write_line("PONG %s" % tuple['args'][0])

    def handle_privmsg(self, tuple):
        global clientlist

        if tuple['args'][0][0] != '#':
            pass

        # convert to nenolod/irc.staticbox.net
        origin = tuple['origin'][:tuple['origin'].find('!')] + "/" + self.sock.friendlyname

        # build info tuple.
        vchan = self.sock.vchans[tuple['args'][0]]
        if tuple['args'][1].startswith('\x01ACTION ') and tuple['args'][1][-1] == '\x01':
            action = True
            tuple['args'][1] = tuple['args'][1][8:-1]
        else:
            action = False
        info = {'origin': origin, 'target': vchan, 'message': tuple['args'][1], 'action': action}
        for i in clientlist:
            if i.sock == self.sock:
                continue

            i.handle_channel_message(info)

    # actions
    def join_channel(self, channel):
        self.sock.write_line("JOIN %s" % channel)

    def send_to_channel(self, channel, message):
        self.sock.write_line("PRIVMSG %s :%s" % (channel, message))

    # events
    def handle_channel_message(self, info):
    	if info['action']:
	        self.send_to_channel(self.sock.channels[info['target']], "* %s %s" % (info['origin'], info['message']))
        else:
	        self.send_to_channel(self.sock.channels[info['target']], "<%s> %s" % (info['origin'], info['message']))

if __name__ == '__main__':
    p = protocol_base(None)
    print p.parse(":lol!lol@lol PRIVMSG #lol :lol test\r\n");
    print p.parse(":irc.lol.com 001 lol :Welcome to IRC lol\r\n");
    print p.parse("002 lol moocows\r\n");


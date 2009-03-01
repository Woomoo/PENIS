#!/usr/bin/python

import asyncore
import penis.ircsocket
from penis.protocol import rfc1459_client

sb = penis.ircsocket.ircconn('irc.staticbox.net', 6667, 'penis-rfc1459', protocol_handler=rfc1459_client)

asyncore.loop()


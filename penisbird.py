#!/usr/bin/python

import asyncore
import penis.ircsocket
from penis.protocol import rfc1459_client

sb = penis.ircsocket.ircconn('irc.systeminplace.net', 6667, 'rxmirror', protocol_handler=rfc1459_client, channels={ 'yXnVlqV': '#rapidxen' }, friendlyname='staticbox')
sb2 = penis.ircsocket.ircconn('irc.freenode.net', 6667, 'rxmirror', protocol_handler=rfc1459_client, channels={ 'yXnVlqV': '#rapidxen' }, friendlyname='freenode')

asyncore.loop()


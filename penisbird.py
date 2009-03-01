#!/usr/bin/python

import asyncore
import penis.ircsocket
from penis.protocol import rfc1459_client

sb = penis.ircsocket.ircconn('irc.systeminplace.net', 6667, 'mirror1', protocol_handler=rfc1459_client, channels={ 'yXnVlqV': '#rapidxen' })
sb2 = penis.ircsocket.ircconn('irc.staticbox.net', 6667, 'mirror2', protocol_handler=rfc1459_client, channels={ 'yXnVlqV': '#cryptwizard' })

asyncore.loop()


#!/usr/bin/python

import asyncore
import penis.ircsocket
from penis.protocol import rfc1459_client

penis.ircsocket.ircconn('irc.staticbox.net', 6667, 'relaybot', protocol_handler=rfc1459_client, channels={ 'yXnVlqV': '#unicorncastle' }, friendlyname='staticbox')
penis.ircsocket.ircconn('irc.woomoo.org', 6667, 'relaybot', protocol_handler=rfc1459_client, channels={ 'yXnVlqV': '#woomoo' }, friendlyname='woomoo')

asyncore.loop()


#!/usr/bin/env python
from config import ADDRESS

"""
An example to show receiving events from an Event Hub partition.
"""

# pylint: disable=C0111

import sys
import logging
from eventhubs import EventHubClient, Sender, EventData

import examples
logger = examples.get_logger(logging.INFO)

try:

    sender = Sender()
    client = EventHubClient(ADDRESS if len(sys.argv) == 1 else sys.argv[1]) \
                 .publish(sender) \
                 .run_daemon()

    for i in range(2):
        msg = "hello1 " + str(i)
        sender.send(EventData(msg))
        logger.info("Send message %s", msg)

    client.stop()

except KeyboardInterrupt:
    pass

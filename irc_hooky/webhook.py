from abc import ABCMeta
from abc import abstractmethod
import logging


class Webhook(object):
    __metaclass__ = ABCMeta

    def __init__(self, event, context):
        self.log = logging.getLogger("irchooky")
        self.event = event
        self.context = context
        self.irc_message = ""

    @abstractmethod
    def process_event(self):  # pragma: no cover
        pass

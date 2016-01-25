import logging
import irc.client


class IRCClient(object):

    def __init__(self, network, port, nickname):
        self.log = logging.getLogger("irchooky")
        self.network = network
        self.port = port
        self.nickname = nickname
        self.server = None
        self.client = None
        self.channel = ""
        self.message = ""
        self.has_quit = False
        if not self.nickname:
            self.nickname = "irchooky"

    def connect(self):  # pragma: no cover
        self.client = irc.client.Reactor()
        self.log.info("Connecting to IRC network %s" % self.network)
        try:
            self.server = self.client.server()
            self.server.connect(self.network,
                                self.port,
                                self.nickname)
            return True
        except irc.client.ServerConnectionError as x:
            self.log.error(x)
            return False

    def send_msg(self, msg, channel):
        if not msg:
            self.log.error("Invalid message")
            return
        self.message = msg

        if not channel:
            self.log.error("Invalid channel name")
            return
        self.channel = channel

        self.server.add_global_handler("join", self.irc_on_join)
        self.server.add_global_handler("welcome", self.irc_on_connect)
        self.server.add_global_handler("passwdmismatch",
                                       self.irc_on_passwdmismatch)
        self.server.add_global_handler("disconnect", self.irc_on_disconnect)
        self.main_loop()

    def main_loop(self):  # pragma: no cover
        while not self.has_quit:
            self.client.process_once(0.2)

    def irc_on_join(self, connection, event):  # pragma: no cover
        self.log.info("Joined IRC channel %s" % self.channel)
        self.log.info("Sending IRC message %s" % self.message)
        connection.privmsg(self.channel, self.message)
        connection.quit()

    def irc_on_passwdmismatch(self, connection, event):  # pragma: no cover
        self.log.error("Password required")
        self.has_quit = True

    def irc_on_connect(self, connection, event):  # pragma: no cover
        self.log.info("Connected to IRC network.")
        connection.join(self.channel)

    def irc_on_disconnect(self, connection, event):  # pragma: no cover
        self.log.info("Disconnecting from IRC network.")
        self.has_quit = True

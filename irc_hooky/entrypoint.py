import logging
from irc_hooky.github.github_webhook import GithubWebhook
from irc_hooky.irc_client import IRCClient
import json

__version__ = "0.0.1"
logging.basicConfig()
logger = logging.getLogger("irchooky")
logger.setLevel(logging.INFO)


def handler(event, context):
    resource_path = event.get('resource-path')
    if resource_path == "/github":
        handle_github_event(event, context)
    return json.dumps({"version": __version__})


def handle_github_event(event, context):
    logger.debug("Received a request on the /github endpoint")
    gh = GithubWebhook(event, context)
    gh.process_event()
    irc_msg = gh.irc_message
    logger.info(irc_msg)
    send_irc_msg(server=event.get('irc-server'),
                 port=event.get('irc-port'),
                 nickname=event.get('irc-nickname'),
                 channel=event.get('irc-channel'),
                 message=irc_msg)


def send_irc_msg(server, port, nickname, channel, message):
    irc_client = IRCClient(server, port, nickname)
    if not irc_client.connect():
        logger.error("Error connecting to IRC network")
        return
    irc_client.send_msg(message, channel)

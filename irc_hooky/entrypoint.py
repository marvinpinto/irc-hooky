import logging
from irc_hooky.github.github_webhook import GithubWebhook

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    resource_path = event.get('resource-path')
    if resource_path == "/github":
        logger.debug("Received a request on the /github endpoint")
        gh = GithubWebhook(event, context)
        gh.process_event()
        irc_msg = gh.get_irc_message()
        logger.info(irc_msg)
    return '{"success": true}'

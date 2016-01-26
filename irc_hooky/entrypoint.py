import logging
from irc_hooky.github.github_webhook import GithubWebhook
from irc_hooky.irc_client import IRCClient
import json
import boto3

__version__ = "0.0.3"
logging.basicConfig()
logger = logging.getLogger("irchooky")
logger.setLevel(logging.INFO)


def handler(event, context):
    json_version = json.dumps({"version": __version__})
    logger.debug("Received event: %s" % event)

    if is_sns_event(event):
        send_irc_msg(event, context)
        return json_version

    resource_path = event.get('resource-path')
    if resource_path == "/github":
        handle_github_event(event, context)

    return json_version


def is_sns_event(event):
    """
    Determine if the event we just received is an SNS event
    """
    if "Records" in event:
        return True
    return False


def handle_github_event(event, context):
    logger.debug("Received a request on the /github endpoint")
    gh = GithubWebhook(event, context)
    gh.process_event()
    irc_msg = gh.irc_message
    logger.info(irc_msg)
    event.update({'irc-message': irc_msg})
    send_sns_msg(event, context)


def send_sns_msg(event, context):
    message = {
        "irc-server": event.get('irc-server'),
        "irc-port": event.get('irc-port'),
        "irc-channel": event.get('irc-channel'),
        "irc-nickname": event.get('irc-nickname'),
        "irc-message": event.get('irc-message')
    }
    logger.info("Will publish message to SNS: %s" % json.dumps(message))
    client = boto3.client('sns')
    response = client.publish(TopicArn=event.get('irchooky-sns-arn'),
                              Message=json.dumps(message))
    logger.info("SNS publish result: %s" % response)


def send_irc_msg(event, context):
    logger.debug("Received an SNS event: %s" % json.dumps(event))

    # This is going to hurt if there are more than one irc messages needing to
    # be delivered, in the same SNS payload. Something to optimize for perhaps
    # later.

    for record in event['Records']:
        msg_str = record['Sns'].get('Message')
        msg_json = json.loads(msg_str)
        logger.debug("Record: %s" % msg_json)

        irc_client = IRCClient(network=msg_json.get('irc-server'),
                               port=msg_json.get('irc-port'),
                               nickname=msg_json.get('irc-nickname'))
        irc_client.connect()
        irc_client.send_msg(msg=msg_json.get('irc-message'),
                            channel=msg_json.get('irc-channel'))

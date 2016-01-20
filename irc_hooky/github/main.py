import logging
from irc_hooky.github.github_issue_event import GithubIssueEvent

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):  # pragma: no cover
    event_type = event.get('X-Github-Event')
    irc_msg = ""
    if event_type == "issues":
        logger.debug("Received a Github Issue event")
        irc_msg = process_github_issue_event(event.get('gh-payload'))
    logger.info(irc_msg)
    return "Done!"


def process_github_issue_event(payload):
    if not payload:
        logger.error("Received an empty payload as an issue event")
        return ""
    issue_event = GithubIssueEvent()
    issue_event.load(payload)
    logger.debug("issue event is: %s" % issue_event)
    return get_issue_event_irc_notification_msg(issue_event)


def get_issue_event_irc_notification_msg(issue_event):
    title = issue_event.issue.title
    action = issue_event.action

    user = "Nobody"
    if issue_event.sender.login:
        user = issue_event.sender.login

    assignee = "Nobody"
    if issue_event.issue.assignee.login:
        assignee = issue_event.issue.assignee.login

    labels = "None"
    if issue_event.issue.labels:
        str_labels = []
        for label in issue_event.issue.labels:
            str_labels.append(label.name)
        labels = ",".join(str_labels)

    url = "<No URL Specified>"
    if issue_event.issue.html_url:
        url = issue_event.issue.html_url

    msg = []
    msg.append("GitHub Issue")
    msg.append("\"%s\"" % title)
    msg.append("%s by %s" % (action, user))
    msg.append("(Assigned to: %s, Labels: %s)" % (assignee, labels))
    msg.append(url)
    return " ".join(msg)

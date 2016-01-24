from irc_hooky.github.github_issue_event import GithubIssueEvent
from irc_hooky.webhook import Webhook


class GithubWebhook(Webhook):

    def __init__(self, event, context):
        super(GithubWebhook, self).__init__(event, context)

    def process_event(self):
        payload = self.event.get('payload')
        if not payload:
            self.log.error("Received an empty github payload")
            return

        event_type = self.event.get('X-Github-Event')
        if event_type == "issues":
            self.log.debug("Received a Github Issue event")
            self.irc_message = self.process_github_issue_event(payload)

    def process_github_issue_event(self, payload):
        issue_event = GithubIssueEvent()
        issue_event.load(payload)
        self.log.debug("Issue event is: %s" % issue_event)
        return_msg = self.get_issue_event_irc_notification_msg(issue_event)
        self.log.debug("Issue event IRC msg: %s" % return_msg)
        return return_msg

    def get_issue_event_irc_notification_msg(self, issue_event):
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

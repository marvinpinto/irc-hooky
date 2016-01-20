from irc_hooky.base_object import BaseObject
from irc_hooky.github.github_user import GithubUser
from irc_hooky.github.github_issue import GithubIssue


class GithubIssueEvent(BaseObject):

    properties = [
        'action',
        'issue',
        'sender'
    ]

    def __init__(self, **kwargs):
        super(GithubIssueEvent, self).__init__(**kwargs)
        self.action = "<No Action Specified>"

    def load(self, object_dict):
        self.action = object_dict.get('action', self.action)

        gh_issue = object_dict.get('issue', None)
        self.issue = GithubIssue()
        if gh_issue:
            self.issue.load(gh_issue)

        gh_user = object_dict.get('sender', None)
        self.sender = GithubUser()
        if gh_user:
            self.sender.load(gh_user)

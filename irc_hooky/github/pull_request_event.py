from irc_hooky.base_object import BaseObject
from irc_hooky.github.github_user import GithubUser
from irc_hooky.github.pull_request import PullRequest


class PullRequestEvent(BaseObject):

    properties = [
        'action',
        'number',
        'pull_request',
        'sender'
    ]

    def __init__(self, **kwargs):
        super(PullRequestEvent, self).__init__(**kwargs)
        self.action = "<No Action Specified>"
        self.pull_request = PullRequest()
        self.sender = GithubUser()

    def load(self, object_dict):
        self.action = object_dict.get('action', self.action)
        self.number = object_dict.get('number', self.number)

        gh_pr = object_dict.get('pull_request', None)
        self.pull_request = PullRequest()
        if gh_pr:
            self.pull_request.load(gh_pr)

        gh_user = object_dict.get('sender', None)
        self.sender = GithubUser()
        if gh_user:
            self.sender.load(gh_user)

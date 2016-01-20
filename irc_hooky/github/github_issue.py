from irc_hooky.base_object import BaseObject
from irc_hooky.github.github_user import GithubUser
from irc_hooky.github.github_issue_label import GithubIssueLabel


class GithubIssue(BaseObject):

    properties = [
        'title',
        'html_url',
        'assignee',
        'state',
        'labels',
        'user'
    ]

    def __init__(self, **kwargs):
        super(GithubIssue, self).__init__(**kwargs)
        if not self.title:
            self.title = "No Title"
        if not self.assignee:
            self.assignee = GithubUser()
        if not self.labels:
            self.labels = []
        if not self.user:
            self.user = GithubUser()

    def load(self, object_dict):
        for prop in ["title", "html_url", "state"]:
            default = getattr(self, prop)
            setattr(self, prop, object_dict.get(prop, default))

        gh_assignee = object_dict.get('assignee', None)
        self.assignee = GithubUser()
        if gh_assignee:
            self.assignee.load(gh_assignee)

        gh_labels = object_dict.get('labels', [])
        self.labels = []
        for label in gh_labels:
            t_label = GithubIssueLabel()
            t_label.load(label)
            self.labels.append(t_label)

        gh_user = object_dict.get('user', None)
        self.user = GithubUser()
        if gh_user:
            self.user.load(gh_user)

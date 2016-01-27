from irc_hooky.base_object import BaseObject
from irc_hooky.github.github_user import GithubUser


class PullRequest(BaseObject):

    properties = [
        'html_url',
        'state',
        'title',
        'user',
        'merged'
    ]

    def __init__(self, **kwargs):
        super(PullRequest, self).__init__(**kwargs)
        if not self.title:
            self.title = "[No Title]"
        if not self.user:
            self.user = GithubUser()
        if not self.merged:
            self.merged = False

    def load(self, object_dict):
        for prop in ["title", "html_url", "state", "merged"]:
            default = getattr(self, prop)
            setattr(self, prop, object_dict.get(prop, default))

        gh_user = object_dict.get('user', None)
        self.user = GithubUser()
        if gh_user:
            self.user.load(gh_user)

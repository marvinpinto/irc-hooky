from irc_hooky.base_object import BaseObject


class GithubIssueLabel(BaseObject):

    properties = [
        'url',
        'name',
        'color'
    ]

    def __init__(self, **kwargs):
        super(GithubIssueLabel, self).__init__(**kwargs)

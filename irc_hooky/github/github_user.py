from irc_hooky.base_object import BaseObject


class GithubUser(BaseObject):

    properties = [
        'login',
        'html_url'
    ]

    def __init__(self, **kwargs):
        super(GithubUser, self).__init__(**kwargs)

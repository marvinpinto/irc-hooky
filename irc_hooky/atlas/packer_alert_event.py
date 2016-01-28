from irc_hooky.base_object import BaseObject


class PackerAlertEvent(BaseObject):

    properties = [
        'build_configuration',
        'number',
        'status',
        'url'
    ]

    def __init__(self, **kwargs):
        super(PackerAlertEvent, self).__init__(**kwargs)

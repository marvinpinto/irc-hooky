from irc_hooky.base_object import BaseObject


class TerraformAlertEvent(BaseObject):

    properties = [
        'environment',
        'message',
        'number',
        'status',
        'url'
    ]

    def __init__(self, **kwargs):
        super(TerraformAlertEvent, self).__init__(**kwargs)

from irc_hooky.webhook import Webhook
from irc_hooky.atlas.terraform_alert_event import TerraformAlertEvent
from irc_hooky.atlas.packer_alert_event import PackerAlertEvent


class AtlasWebhook(Webhook):

    def __init__(self, event, context):
        super(AtlasWebhook, self).__init__(event, context)

    def process_event(self):
        payload = self.event.get('payload')
        if not payload:
            self.log.error("Received an empty atlas payload")
            return

        event_type = self.get_atlas_event_type(payload)
        if event_type == "terraform_alert":
            self.log.debug("Received an Atlas Terraform alert")
            self.irc_message = self.process_atlas_tf_event(payload)
        elif event_type == "packer_alert":
            self.log.debug("Received an Atlas Packer alert")
            self.irc_message = self.process_atlas_packer_event(payload)
        else:
            self.log.info("Could not determine Atlas event type")
            self.irc_message = ""

    def get_atlas_event_type(self, payload):
        for event_type in ['terraform_alert', 'packer_alert']:
            if event_type in payload:
                return event_type
        return ""

    def process_atlas_packer_event(self, payload):
        packer_event = PackerAlertEvent()
        packer_event.load(payload['packer_alert'])
        self.log.debug("Packer event is: %s" % packer_event)
        return_msg = self.get_packer_event_irc_notification_msg(packer_event)
        self.log.debug("Packer event IRC msg: %s" % return_msg)
        return return_msg

    def get_packer_event_irc_notification_msg(self, packer_event):
        # Messaging roughly looks like:
        # Packer build has begun. http://url.com
        # Packer build finished successfully! http://url.com
        # An error occurred during the Packer build. http://url.com
        # Packer build was cancelled. http://url.com

        msg = []
        status = packer_event.status

        if status == "started":
            msg.append("Packer build has begun.")
        elif status == "finished":
            msg.append("Packer build finished successfully!")
        elif status == "canceled":
            msg.append("Packer build was cancelled.")
        elif status == "errored":
            msg.append("An error occurred during the Packer build.")
        else:
            self.log.info("Encountered an unknown Packer event: %s" % status)
            return ""

        msg.append(packer_event.url)
        return " ".join(msg)

    def process_atlas_tf_event(self, payload):
        tf_event = TerraformAlertEvent()
        tf_event.load(payload['terraform_alert'])
        self.log.debug("Terraform event is: %s" % tf_event)
        return_msg = self.get_tf_event_irc_notification_msg(tf_event)
        self.log.debug("Terraform event IRC msg: %s" % return_msg)
        return return_msg

    def get_tf_event_irc_notification_msg(self, tf_event):
        # Messaging roughly looks like:
        # Terraform plan needs confirmation. http://url.com
        # Terraform plan was applied successfully! http://url.com
        # An error occurred during the Terraform plan or apply phase. http://url.com  # NOQA

        msg = []
        status = tf_event.status

        if status == "planned":
            msg.append("Terraform plan needs confirmation.")
        elif status == "applied":
            msg.append("Terraform plan was applied successfully!")
        elif status == "errored":
            msg.append("An error occurred during the Terraform plan or apply phase.")  # NOQA
        else:
            self.log.info("Encountered an unknown Terraform event: %s" % status)  # NOQA
            return ""

        msg.append(tf_event.url)
        return " ".join(msg)

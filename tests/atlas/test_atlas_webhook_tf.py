import unittest
from irc_hooky.atlas.atlas_webhook import AtlasWebhook


class TestAtlasWebhookTerraform(unittest.TestCase):

    def test_empty_payload(self):
        payload = {}
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        self.assertEqual(atl.irc_message, "")

    def test_process_non_atl_event(self):
        payload = {
            "foo": "bar"
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        self.assertEqual(atl.irc_message, "")

    def test_process_invalid_atl_event(self):
        payload = {
            "fake_alert": {
                "environment": "user/tf-test",
                "message": "Queued manually in Atlas",
                "number": 2,
                "status": "errored",
                "url": "https://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        self.assertEqual(atl.irc_message, "")

    def test_unknown_tf_event(self):
        payload = {
            "terraform_alert": {
                "environment": "user/tf-test",
                "message": "Queued manually in Atlas",
                "number": 2,
                "status": "fakestatus",
                "url": "https://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        self.assertEqual(atl.irc_message, "")

    def test_tf_needs_confirmation_event(self):
        payload = {
            "terraform_alert": {
                "environment": "user/tf-test",
                "message": "Queued manually in Atlas",
                "number": 2,
                "status": "planned",
                "url": "https://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        expected_msg = "Terraform plan needs confirmation. https://url.com"
        self.assertEqual(atl.irc_message, expected_msg)

    def test_tf_applied_event(self):
        payload = {
            "terraform_alert": {
                "environment": "user/tf-test",
                "message": "Queued manually in Atlas",
                "number": 2,
                "status": "applied",
                "url": "https://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        expected_msg = "Terraform plan was applied successfully! https://url.com"  # NOQA
        self.assertEqual(atl.irc_message, expected_msg)

    def test_tf_errored_event(self):
        payload = {
            "terraform_alert": {
                "environment": "user/tf-test",
                "message": "Queued manually in Atlas",
                "number": 2,
                "status": "errored",
                "url": "https://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        expected_msg = "An error occurred during the Terraform plan or apply phase. https://url.com"  # NOQA
        self.assertEqual(atl.irc_message, expected_msg)

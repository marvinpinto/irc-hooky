import unittest
from irc_hooky.atlas.atlas_webhook import AtlasWebhook


class TestAtlasWebhookPacker(unittest.TestCase):

    def test_unknown_packer_event(self):
        payload = {
            "packer_alert": {
                "build_configuration": "marvinpinto/packer-test",
                "number": 2,
                "status": "fakestatus",
                "url": "http://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        self.assertEqual(atl.irc_message, "")

    def test_packer_started_event(self):
        payload = {
            "packer_alert": {
                "build_configuration": "marvinpinto/packer-test",
                "number": 2,
                "status": "started",
                "url": "http://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        expected_msg = "Packer build has begun. http://url.com"
        self.assertEqual(atl.irc_message, expected_msg)

    def test_packer_finished_event(self):
        payload = {
            "packer_alert": {
                "build_configuration": "marvinpinto/packer-test",
                "number": 2,
                "status": "finished",
                "url": "http://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        expected_msg = "Packer build finished successfully! http://url.com"
        self.assertEqual(atl.irc_message, expected_msg)

    def test_packer_canceled_event(self):
        payload = {
            "packer_alert": {
                "build_configuration": "marvinpinto/packer-test",
                "number": 2,
                "status": "canceled",
                "url": "http://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        expected_msg = "Packer build was cancelled. http://url.com"
        self.assertEqual(atl.irc_message, expected_msg)

    def test_packer_errored_event(self):
        payload = {
            "packer_alert": {
                "build_configuration": "marvinpinto/packer-test",
                "number": 2,
                "status": "errored",
                "url": "http://url.com"
            }
        }
        event = {
            "payload": payload
        }
        atl = AtlasWebhook(event, {})
        self.assertEqual(atl.irc_message, "")
        atl.process_event()
        expected_msg = "An error occurred during the Packer build. http://url.com"  # NOQA
        self.assertEqual(atl.irc_message, expected_msg)

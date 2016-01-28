import unittest
import json
from mock import patch
from irc_hooky.entrypoint import handler


class TestEntrypoint(unittest.TestCase):

    def setUp(self):
        patcher1 = patch('irc_hooky.entrypoint.send_irc_msg')
        self.addCleanup(patcher1.stop)
        self.mock_send_irc_msg = patcher1.start()

        patcher2 = patch('irc_hooky.entrypoint.send_sns_msg')
        self.addCleanup(patcher2.stop)
        self.mock_send_sns_msg = patcher2.start()

    def test_valid_sns_event(self):
        event = {
            "Records": [
                {
                    "number": "1"
                }
            ]
        }
        result = json.loads(handler(event, {}))
        self.assertTrue(result['version'])
        self.assertEqual(len(self.mock_send_irc_msg.mock_calls), 1)
        self.assertEqual(len(self.mock_send_sns_msg.mock_calls), 0)

    def test_invalid_resource_path(self):
        event = {
            "X-Hub-Signature": "",
            "X-Github-Event": "pull_request",
            "resource-path": "/invalid",
            "irc-server": "chat.freenode.net",
            "irc-port": 6667,
            "irc-channel": "##testtest",
            "irchooky-sns-arn": "arn",
            "payload": {}
        }
        result = json.loads(handler(event, {}))
        self.assertTrue(result['version'])
        self.assertEqual(len(self.mock_send_irc_msg.mock_calls), 0)
        self.assertEqual(len(self.mock_send_sns_msg.mock_calls), 0)

    def test_invalid_github_event_type(self):
        event = {
            "X-Hub-Signature": "",
            "X-Github-Event": "fake_event",
            "resource-path": "/github",
            "irc-server": "chat.freenode.net",
            "irc-port": 6667,
            "irc-channel": "##testtest",
            "irchooky-sns-arn": "arn",
            "payload": {}
        }
        result = json.loads(handler(event, {}))
        self.assertTrue(result['version'])
        self.assertEqual(len(self.mock_send_irc_msg.mock_calls), 0)
        self.assertEqual(len(self.mock_send_sns_msg.mock_calls), 0)

    def test_valid_github_event_type(self):
        event = {
            "X-Hub-Signature": "",
            "X-Github-Event": "pull_request",
            "resource-path": "/github",
            "irc-server": "chat.freenode.net",
            "irc-port": 6667,
            "irc-channel": "##testtest",
            "irchooky-sns-arn": "arn",
            "payload": {
                "hello": "hi"
            }
        }
        result = json.loads(handler(event, {}))
        self.assertTrue(result['version'])
        self.assertEqual(len(self.mock_send_irc_msg.mock_calls), 0)
        self.assertEqual(len(self.mock_send_sns_msg.mock_calls), 1)

    def test_valid_atlas_event_type(self):
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
            "X-Hub-Signature": "",
            "X-Github-Event": "pull_request",
            "resource-path": "/atlas",
            "irc-server": "chat.freenode.net",
            "irc-port": 6667,
            "irc-channel": "##testtest",
            "irchooky-sns-arn": "arn",
            "payload": payload
        }
        result = json.loads(handler(event, {}))
        self.assertTrue(result['version'])
        self.assertEqual(len(self.mock_send_irc_msg.mock_calls), 0)
        self.assertEqual(len(self.mock_send_sns_msg.mock_calls), 1)

import unittest
from mock import MagicMock
from mock import call
from irc_hooky.irc_client import IRCClient


class TestIRCClient(unittest.TestCase):

    def setUp(self):
        self.client = IRCClient("foo.bar.net",
                                1234,
                                "nickname")
        self.client.main_loop = MagicMock()
        self.client.server = MagicMock()

    def test_nicknames(self):
        self.assertEqual(self.client.nickname, "nickname")
        self.client = IRCClient("foo.bar.net", 1234, "")
        self.assertEqual(self.client.nickname, "irchooky")

    def test_send_empty_msg(self):
        with self.assertRaises(Exception):
            self.client.send_msg("", "#channel")

    def test_send_empty_channel(self):
        with self.assertRaises(Exception):
            self.client.send_msg("message", "")

    def test_send_msg(self):
        self.client.send_msg("message", "#channel")
        self.assertEqual(self.client.main_loop.mock_calls, [call()])
        self.assertEqual(len(self.client.server.mock_calls), 4)

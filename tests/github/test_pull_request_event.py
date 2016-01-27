import unittest
from irc_hooky.github.pull_request import PullRequest
from irc_hooky.github.pull_request_event import PullRequestEvent
from irc_hooky.github.github_user import GithubUser


class TestPullRequestEvent(unittest.TestCase):

    def setUp(self):
        self.ghpre = PullRequestEvent()

    def test_default_setup(self):
        self.assertEqual(self.ghpre.action, "<No Action Specified>")
        self.assertEqual(self.ghpre.number, "")
        self.assertEqual(self.ghpre.pull_request, PullRequest())
        self.assertEqual(self.ghpre.sender, GithubUser())

    def test_load_empty_secondary_objects(self):
        payload = {}
        self.ghpre.load(payload)
        self.assertEqual(self.ghpre.action, "<No Action Specified>")
        self.assertEqual(self.ghpre.number, "")
        self.assertEqual(self.ghpre.pull_request, PullRequest())
        self.assertEqual(self.ghpre.sender, GithubUser())

    def test_non_empty_pr(self):
        payload = {
            "action": "sleep",
            "pull_request": {
                "title": "new pr"
            }
        }
        self.ghpre.load(payload)
        self.assertEqual(self.ghpre.action, "sleep")
        self.assertEqual(self.ghpre.number, "")
        self.assertEqual(self.ghpre.pull_request, PullRequest(title="new pr"))
        self.assertEqual(self.ghpre.sender, GithubUser())

    def test_non_empty_sender(self):
        payload = {
            "action": "sleep",
            "number": "42",
            "pull_request": {
                "title": "new pr"
            },
            "sender": {
                "login": "steven"
            }
        }
        self.ghpre.load(payload)
        self.assertEqual(self.ghpre.action, "sleep")
        self.assertEqual(self.ghpre.number, "42")
        self.assertEqual(self.ghpre.pull_request, PullRequest(title="new pr"))
        self.assertEqual(self.ghpre.sender, GithubUser(login="steven"))

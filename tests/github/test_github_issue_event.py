import unittest
from irc_hooky.github.github_issue import GithubIssue
from irc_hooky.github.github_issue_event import GithubIssueEvent
from irc_hooky.github.github_user import GithubUser


class TestGithubIssueEvent(unittest.TestCase):

    def setUp(self):
        self.ghie = GithubIssueEvent()

    def test_default_setup(self):
        self.assertEqual(self.ghie.action, "<No Action Specified>")
        self.assertEqual(self.ghie.issue, "")
        self.assertEqual(self.ghie.sender, "")

    def test_load_empty_secondary_objects(self):
        payload = {}
        self.ghie.load(payload)
        self.assertEqual(self.ghie.action, "<No Action Specified>")
        self.assertEqual(self.ghie.issue, GithubIssue())
        self.assertEqual(self.ghie.sender, GithubUser())

    def test_non_empty_issue(self):
        payload = {
            "action": "sleep",
            "issue": {
                "title": "new issue"
            }
        }
        self.ghie.load(payload)
        self.assertEqual(self.ghie.action, "sleep")
        self.assertEqual(self.ghie.issue, GithubIssue(title="new issue"))
        self.assertEqual(self.ghie.sender, GithubUser())

    def test_non_empty_sender(self):
        payload = {
            "action": "sleep",
            "issue": {
                "title": "new issue"
            },
            "sender": {
                "login": "steven"
            }
        }
        self.ghie.load(payload)
        self.assertEqual(self.ghie.action, "sleep")
        self.assertEqual(self.ghie.issue, GithubIssue(title="new issue"))
        self.assertEqual(self.ghie.sender, GithubUser(login="steven"))

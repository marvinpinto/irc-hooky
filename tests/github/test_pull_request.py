import unittest
from irc_hooky.github.pull_request import PullRequest
from irc_hooky.github.github_user import GithubUser


class TestPullRequest(unittest.TestCase):

    def setUp(self):
        self.ghpr = PullRequest()

    def test_default_setup(self):
        self.assertEqual(self.ghpr.title, "[No Title]")
        self.assertEqual(self.ghpr.html_url, "")
        self.assertEqual(self.ghpr.state, "")
        self.assertEqual(self.ghpr.merged, False)
        self.assertEqual(self.ghpr.user, GithubUser())

    def test_load_empty_secondary_objects(self):
        payload = {}
        self.ghpr.load(payload)
        self.assertEqual(self.ghpr.title, "[No Title]")
        self.assertEqual(self.ghpr.html_url, "")
        self.assertEqual(self.ghpr.state, "")
        self.assertEqual(self.ghpr.merged, False)
        self.assertEqual(self.ghpr.user, GithubUser())

    def test_non_empty_user(self):
        payload = {
            "user": {
                "login": "u2",
                "html_url": "u2.com"
            },
        }
        self.ghpr.load(payload)
        self.assertEqual(self.ghpr.title, "[No Title]")
        self.assertEqual(self.ghpr.html_url, "")
        self.assertEqual(self.ghpr.state, "")
        self.assertEqual(self.ghpr.merged, False)
        self.assertEqual(self.ghpr.user,
                         GithubUser(login="u2", html_url="u2.com"))

import unittest
from irc_hooky.github.github_issue import GithubIssue
from irc_hooky.github.github_user import GithubUser
from irc_hooky.github.github_issue_label import GithubIssueLabel


class TestGithubIssue(unittest.TestCase):

    def setUp(self):
        self.ghi = GithubIssue()

    def test_default_setup(self):
        self.assertEqual(self.ghi.title, "No Title")
        self.assertEqual(self.ghi.html_url, "")
        self.assertEqual(self.ghi.state, "")
        self.assertEqual(self.ghi.assignee, GithubUser())
        self.assertEqual(self.ghi.labels, [])
        self.assertEqual(self.ghi.user, GithubUser())

    def test_load_empty_secondary_objects(self):
        payload = {}
        self.ghi.load(payload)
        self.assertEqual(self.ghi.title, "No Title")
        self.assertEqual(self.ghi.html_url, "")
        self.assertEqual(self.ghi.state, "")
        self.assertEqual(self.ghi.assignee, GithubUser())
        self.assertEqual(self.ghi.labels, [])
        self.assertEqual(self.ghi.user, GithubUser())

    def test_non_empty_assignee(self):
        payload = {
            "assignee": {
                "login": "marvin",
                "html_url": "http://news.com"
            }
        }
        self.ghi.load(payload)
        self.assertEqual(self.ghi.title, "No Title")
        self.assertEqual(self.ghi.html_url, "")
        self.assertEqual(self.ghi.state, "")
        self.assertEqual(self.ghi.assignee,
                         GithubUser(login="marvin",
                                    html_url="http://news.com"))
        self.assertEqual(self.ghi.labels, [])
        self.assertEqual(self.ghi.user, GithubUser())

    def test_single_label(self):
        payload = {
            "assignee": {
                "login": "marvin",
                "html_url": "http://news.com"
            },
            "labels": [
                {
                    "url": "label.com",
                    "name": "label name",
                    "color": "red"
                }
            ]
        }
        expected_labels = [
            GithubIssueLabel(url="label.com", name="label name", color="red")
        ]
        self.ghi.load(payload)
        self.assertEqual(self.ghi.title, "No Title")
        self.assertEqual(self.ghi.html_url, "")
        self.assertEqual(self.ghi.state, "")
        self.assertEqual(self.ghi.assignee,
                         GithubUser(login="marvin",
                                    html_url="http://news.com"))
        self.assertEqual(self.ghi.labels, expected_labels)
        self.assertEqual(self.ghi.user, GithubUser())

    def test_multiple_labels(self):
        payload = {
            "assignee": {
                "login": "marvin",
                "html_url": "http://news.com"
            },
            "labels": [
                {
                    "url": "label.com",
                    "name": "label name",
                    "color": "red"
                },
                {
                    "url": "label2.com",
                    "name": "label2 name",
                    "color": "blue"
                }
            ]
        }
        expected_labels = [
            GithubIssueLabel(url="label.com", name="label name", color="red"),
            GithubIssueLabel(url="label2.com",
                             name="label2 name",
                             color="blue")
        ]
        self.ghi.load(payload)
        self.assertEqual(self.ghi.title, "No Title")
        self.assertEqual(self.ghi.html_url, "")
        self.assertEqual(self.ghi.state, "")
        self.assertEqual(self.ghi.assignee,
                         GithubUser(login="marvin",
                                    html_url="http://news.com"))
        self.assertEqual(self.ghi.labels, expected_labels)
        self.assertEqual(self.ghi.user, GithubUser())

    def test_non_empty_user(self):
        payload = {
            "assignee": {
                "login": "marvin",
                "html_url": "http://news.com"
            },
            "labels": [
                {
                    "url": "label.com",
                    "name": "label name",
                    "color": "red"
                },
                {
                    "url": "label2.com",
                    "name": "label2 name",
                    "color": "blue"
                }
            ],
            "user": {
                "login": "u2",
                "html_url": "u2.com"
            },
        }
        expected_labels = [
            GithubIssueLabel(url="label.com", name="label name", color="red"),
            GithubIssueLabel(url="label2.com",
                             name="label2 name",
                             color="blue")
        ]
        self.ghi.load(payload)
        self.assertEqual(self.ghi.title, "No Title")
        self.assertEqual(self.ghi.html_url, "")
        self.assertEqual(self.ghi.state, "")
        self.assertEqual(self.ghi.assignee,
                         GithubUser(login="marvin",
                                    html_url="http://news.com"))
        self.assertEqual(self.ghi.labels, expected_labels)
        self.assertEqual(self.ghi.user,
                         GithubUser(login="u2", html_url="u2.com"))

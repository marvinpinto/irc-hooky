import unittest
from irc_hooky.github.github_webhook import GithubWebhook


class TestGithubWebhookPullRequest(unittest.TestCase):

    def test_empty_secondary_objects(self):
        payload = {
            "action": "",
            "number": "",
            "pull_request": {},
            "sender": {}
        }
        event = {
            "X-Github-Event": "pull_request",
            "payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Pull Request \"[No Title]\"  by Nobody <No URL Specified>"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_non_empty_user(self):
        payload = {
            "action": "opened",
            "pull_request": {
                "title": "New PR"
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "pull_request",
            "payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Pull Request \"New PR\" opened by mary <No URL Specified>"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_non_empty_url(self):
        payload = {
            "action": "closed",
            "pull_request": {
                "title": "New PR",
                "html_url": "http://news.com"
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "pull_request",
            "payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Pull Request \"New PR\" closed by mary http://news.com"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_merged_pr(self):
        payload = {
            "action": "closed",
            "pull_request": {
                "title": "New PR",
                "html_url": "http://news.com",
                "merged": True
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "pull_request",
            "payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Pull Request \"New PR\" merged by mary http://news.com"  # NOQA
        self.assertEqual(gh.irc_message, expected)

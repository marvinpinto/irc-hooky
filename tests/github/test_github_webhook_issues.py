import unittest
from irc_hooky.github.github_webhook import GithubWebhook


class TestGithubWebhookIssues(unittest.TestCase):

    def test_empty_payload(self):
        payload = {}
        event = {
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        self.assertEqual(gh.irc_message, "")

    def test_process_non_gh_event(self):
        payload = {
            "foo": "bar"
        }
        event = {
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        self.assertEqual(gh.irc_message, "")

    def test_empty_secondary_objects(self):
        payload = {
            "action": "",
            "issue": {},
            "sender": {}
        }
        event = {
            "X-Github-Event": "issues",
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Issue \"No Title\"  by Nobody (Assigned to: Nobody, Labels: None) <No URL Specified>"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_non_empty_user(self):
        payload = {
            "action": "opened",
            "issue": {
                "title": "New Issue"
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "issues",
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: Nobody, Labels: None) <No URL Specified>"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_non_empty_assignee(self):
        payload = {
            "action": "opened",
            "issue": {
                "title": "New Issue",
                "assignee": {
                    "login": "steven"
                }
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "issues",
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: None) <No URL Specified>"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_one_label(self):
        payload = {
            "action": "opened",
            "issue": {
                "title": "New Issue",
                "assignee": {
                    "login": "steven"
                },
                "labels": [
                    {
                        "name": "boog"
                    }
                ]
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "issues",
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: boog) <No URL Specified>"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_two_labels(self):
        payload = {
            "action": "opened",
            "issue": {
                "title": "New Issue",
                "assignee": {
                    "login": "steven"
                },
                "labels": [
                    {
                        "name": "boog"
                    },
                    {
                        "name": "important"
                    }
                ]
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "issues",
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: boog,important) <No URL Specified>"  # NOQA
        self.assertEqual(gh.irc_message, expected)

    def test_non_empty_url(self):
        payload = {
            "action": "opened",
            "issue": {
                "title": "New Issue",
                "assignee": {
                    "login": "steven"
                },
                "html_url": "http://news.com",
                "labels": [
                    {
                        "name": "boog"
                    },
                    {
                        "name": "important"
                    }
                ]
            },
            "sender": {
                "login": "mary"
            }
        }
        event = {
            "X-Github-Event": "issues",
            "gh-payload": payload
        }
        gh = GithubWebhook(event, {})
        self.assertEqual(gh.irc_message, "")
        gh.process_event()
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: boog,important) http://news.com"  # NOQA
        self.assertEqual(gh.irc_message, expected)

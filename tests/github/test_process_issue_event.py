import unittest
from irc_hooky.entrypoint import process_github_issue_event


class TestProcessIssueEvent(unittest.TestCase):

    def test_empty_payload(self):
        payload = {}
        result = process_github_issue_event(payload)
        self.assertEqual(result, "")

    def test_empty_secondary_objects(self):
        payload = {
            "action": "",
            "issue": {},
            "sender": {}
        }
        result = process_github_issue_event(payload)
        expected = "GitHub Issue \"No Title\"  by Nobody (Assigned to: Nobody, Labels: None) <No URL Specified>"  # NOQA
        self.assertEqual(result, expected)

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
        result = process_github_issue_event(payload)
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: Nobody, Labels: None) <No URL Specified>"  # NOQA
        self.assertEqual(result, expected)

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
        result = process_github_issue_event(payload)
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: None) <No URL Specified>"  # NOQA
        self.assertEqual(result, expected)

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
        result = process_github_issue_event(payload)
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: boog) <No URL Specified>"  # NOQA
        self.assertEqual(result, expected)

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
        result = process_github_issue_event(payload)
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: boog,important) <No URL Specified>"  # NOQA
        self.assertEqual(result, expected)

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
        result = process_github_issue_event(payload)
        expected = "GitHub Issue \"New Issue\" opened by mary (Assigned to: steven, Labels: boog,important) http://news.com"  # NOQA
        self.assertEqual(result, expected)

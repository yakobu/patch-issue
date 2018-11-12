from mock import MagicMock

from tests.mock_resources.issue import MockIssue


class MockJira(MagicMock):
    def issue(self, issue_key):
        return MockIssue(issue_key)

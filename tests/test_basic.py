import pytest
from mock import MagicMock

from mock_resources import MockJira
from patch_issue import JiraPatchIssue, RESOLVED_STATUS


@pytest.fixture()
def done_issue():
    class DoneIssue(JiraPatchIssue):
        # We are using issue key in order to define issue status
        ISSUE_KEY = RESOLVED_STATUS
        DESCRIPTION = "This Issue already done"

    return DoneIssue(jira=MockJira(), logger=MagicMock())


def test_patch_done_issue_decorator(done_issue):
    @done_issue.patch_function
    def patch_action():
        pass

    patch_action()

    assert done_issue.logger.warning.call_count == 3

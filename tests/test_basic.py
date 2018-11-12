import pytest
from mock import MagicMock

from .mock_resources import MockJira
from patch_issue import JiraPatchIssue, RESOLVED_STATUS

DONE_DESCRIPTION = "This Issue already done"


@pytest.fixture()
def done_issue():
    class DoneIssue(JiraPatchIssue):
        # We are using issue key in order to define issue status
        ISSUE_KEY = RESOLVED_STATUS
        DESCRIPTION = DONE_DESCRIPTION

    return DoneIssue(jira=MockJira(), logger=MagicMock())


def test_patch_done_issue_decorator(done_issue):
    """Validate patch function on resolved issue."""
    @done_issue.patch_function
    def patch_action():
        pass

    patch_action()

    assert done_issue.logger.warning.call_count == 3
    first_call, second_call, third_call = \
        done_issue.logger.warning.call_args_list

    assert "patch started" in str(first_call)
    assert RESOLVED_STATUS in str(first_call)
    assert DONE_DESCRIPTION in str(second_call)
    assert "patch finished" in str(third_call)


def test_patch_done_issue_context_manager(done_issue):
    """Validate context patch on resolved issue."""
    with done_issue.patch:
        pass

    assert done_issue.logger.warning.call_count == 3
    first_call, second_call, third_call = \
        done_issue.logger.warning.call_args_list

    assert "patch started" in str(first_call)
    assert RESOLVED_STATUS in str(first_call)
    assert DONE_DESCRIPTION in str(second_call)
    assert "patch finished" in str(third_call)

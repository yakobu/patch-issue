from collections import namedtuple

import pytest
from mock import MagicMock

from .mock_resources import MockJira
from patch_issue import JiraPatchIssue, RESOLVED_STATUS

DONE_DESCRIPTION = "This Issue already done"

Issue = namedtuple("Issue", "key description")

ISSUE_CASES = [
    Issue(key=RESOLVED_STATUS, description=DONE_DESCRIPTION),
]


@pytest.fixture(params=ISSUE_CASES)
def tested_issue(request):
    issue = request.param

    class DoneIssue(JiraPatchIssue):
        # We are using issue key in order to define issue status
        ISSUE_KEY = issue.key
        DESCRIPTION = issue.description

    return DoneIssue(jira=MockJira(), logger=MagicMock())


def test_patch_issue_decorator(tested_issue):
    """Validate patch function on given issue."""

    @tested_issue.patch_function
    def patch_action():
        pass

    patch_action()

    assert tested_issue.logger.warning.call_count == 3
    first_call, second_call, third_call = \
        tested_issue.logger.warning.call_args_list

    assert "patch started" in str(first_call)
    assert RESOLVED_STATUS in str(first_call)
    assert DONE_DESCRIPTION in str(second_call)
    assert "patch finished" in str(third_call)


def test_patch_issue_context_manager(tested_issue):
    """Validate context patch on given issue."""
    with tested_issue.patch:
        pass

    assert tested_issue.logger.warning.call_count == 3
    first_call, second_call, third_call = \
        tested_issue.logger.warning.call_args_list

    assert "patch started" in str(first_call)
    assert RESOLVED_STATUS in str(first_call)
    assert DONE_DESCRIPTION in str(second_call)
    assert "patch finished" in str(third_call)

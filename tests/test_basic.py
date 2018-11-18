from collections import namedtuple

import pytest
from attrdict import AttrDict
from mock import MagicMock

from patch_issue import JiraPatchIssue
from patch_issue.mock_resources import MockJira

Issue = namedtuple("Issue", ["key", "description", "resolution",
                             "summary", "status", "way_to_solve"])

ISSUE_CASES = [
    Issue(key="PI-565", description="", way_to_solve="",
          resolution="Done", summary="Done Issue", status="Done"),
    Issue(key="PI-567", description="", way_to_solve="",
          resolution="", summary="in progress issue", status="In Progress"),
    Issue(key="PI-568", description="", way_to_solve="",
          resolution="Wont Do", summary="wont do issue", status="Done"),
    Issue(key="PI-569", description="", way_to_solve="",
          resolution="Done", summary="wont do issue", status="Wont do"),

    Issue(key="PI-575", description="some description", way_to_solve="",
          resolution="Done", summary="Done Issue", status="Done"),
    Issue(key="PI-577", description="some description", way_to_solve="",
          resolution="", summary="in progress issue", status="In Progress"),
    Issue(key="PI-578", description="some description", way_to_solve="",
          resolution="Wont Do", summary="wont do issue", status="Done"),
    Issue(key="PI-579", description="some description", way_to_solve="",
          resolution="Done", summary="wont do issue", status="Wont do"),

    Issue(key="PI-585", description="", way_to_solve="some way",
          resolution="Done", summary="Done Issue", status="Done"),
    Issue(key="PI-587", description="", way_to_solve="some way",
          resolution="", summary="in progress issue", status="In Progress"),
    Issue(key="PI-588", description="", way_to_solve="some way",
          resolution="Wont Do", summary="wont do issue", status="Done"),
    Issue(key="PI-589", description="", way_to_solve="some way",
          resolution="Done", summary="wont do issue", status="Wont do"),

    Issue(key="PI-595", description="some description",
          way_to_solve="some way", resolution="Done",
          summary="Done Issue", status="Done"),
    Issue(key="PI-597", description="some description",
          way_to_solve="some way", resolution="",
          summary="in progress issue", status="In Progress"),
    Issue(key="PI-598", description="some description",
          way_to_solve="some way", resolution="Wont Do",
          summary="wont do issue", status="Done"),
    Issue(key="PI-599", description="some description",
          way_to_solve="some way", resolution="Done",
          summary="wont do issue", status="Wont do"),
]


@pytest.fixture()
def jira():
    issues = AttrDict({})

    for issue in ISSUE_CASES:
        issues[issue.key] = issue

    return MockJira(nown_issues=issues)


@pytest.fixture(params=ISSUE_CASES)
def tested_issue(request, jira):
    issue = request.param

    class TestIssue(JiraPatchIssue):
        ISSUE_KEY = issue.key
        DESCRIPTION = issue.description
        WAY_TO_SOLVE = issue.way_to_solve

    return TestIssue(jira=jira, logger=MagicMock())


def test_patch_issue_decorator(tested_issue, jira):
    """Validate patch function on given issue."""

    @tested_issue.patch_function
    def patch_action():
        pass

    patch_action()

    issue = jira.issue(tested_issue.ISSUE_KEY)
    log_list = tested_issue.logger.warning.call_args_list

    log_arg = str(log_list.pop())
    assert "patch finished" in str(log_arg)
    assert tested_issue.ISSUE_KEY in str(log_arg)

    if tested_issue.WAY_TO_SOLVE and issue.resolution == "Done" and \
                    issue.status == "Done":
        log_arg = str(log_list.pop())
        assert tested_issue.WAY_TO_SOLVE in log_arg

    if tested_issue.DESCRIPTION:
        log_arg = str(log_list.pop())
        assert tested_issue.DESCRIPTION in log_arg

    log_arg = str(log_list.pop())
    assert "patch started" in str(log_arg)
    assert issue.summary in str(log_arg)
    assert issue.status in str(log_arg)


def test_patch_issue_context_manager(tested_issue, jira):
    """Validate context patch on given issue."""
    with tested_issue.patch:
        pass

    issue = jira.issue(tested_issue.ISSUE_KEY)
    log_list = tested_issue.logger.warning.call_args_list

    log_arg = str(log_list.pop())
    assert "patch finished" in str(log_arg)
    assert tested_issue.ISSUE_KEY in str(log_arg)

    if tested_issue.WAY_TO_SOLVE and issue.resolution == "Done" and \
                    issue.status == "Done":
        log_arg = str(log_list.pop())
        assert tested_issue.WAY_TO_SOLVE in log_arg

    if tested_issue.DESCRIPTION:
        log_arg = str(log_list.pop())
        assert tested_issue.DESCRIPTION in log_arg

    log_arg = str(log_list.pop())
    assert "patch started" in str(log_arg)
    assert issue.summary in str(log_arg)
    assert issue.status in str(log_arg)

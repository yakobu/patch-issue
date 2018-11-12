from attrdict import AttrDict
from mock import MagicMock
from property_manager import cached_property

from patch_issue import RESOLVED_STATUS


class MockIssue(MagicMock):
    def __init__(self, issue_key, *args, **kwargs):
        super(MockIssue, self).__init__(*args, **kwargs)
        self.issue_key = issue_key

    @cached_property
    def fields(self):
        resolution = AttrDict({})
        status = AttrDict({"statusCategory":
                               AttrDict({"name": "ToDo"})})

        if self.issue_key == RESOLVED_STATUS:
            resolution.name = RESOLVED_STATUS
            status.statusCategory.name = RESOLVED_STATUS

        return AttrDict({
            "resolution": resolution,
            "summary": "test fields",
            "status": status
        })

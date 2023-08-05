# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from collections import namedtuple

from swh.graphql.backends import archive
from swh.graphql.utils import utils
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseNode


class SnapshotBranchNode(BaseNode):
    """
    Node resolver for a snapshot branch
    """

    # target field for this Node is a UNION type
    # It is resolved in the top level (resolvers.resolvers.py)

    def _get_node_from_data(self, node_data):
        # node_data is not a dict in this case
        # overriding to support this special data structure

        # STORAGE-TODO; return an object in the normal format
        branch_name, branch_obj = node_data
        node = {
            "name": branch_name,
            "type": branch_obj.target_type.value,
            "target": branch_obj.target,
        }
        return namedtuple("NodeObj", node.keys())(*node.values())

    @property
    def target_hash(self):
        return self._node.target


class SnapshotBranchConnection(BaseConnection):
    """
    Connection resolver for the branches in a snapshot
    """

    from .snapshot import SnapshotNode

    obj: SnapshotNode

    _node_class = SnapshotBranchNode

    def _get_paged_result(self) -> PagedResult:
        result = archive.Archive().get_snapshot_branches(
            self.obj.swhid.object_id,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
            target_types=self.kwargs.get("types"),
            name_include=self._get_name_include_arg(),
        )

        # endCursor is the last branch name, logic for that
        end_cusrsor = (
            result["next_branch"] if result["next_branch"] is not None else None
        )
        # FIXME, this pagination is not consistent with other connections
        # FIX in swh-storage to return PagedResult
        # STORAGE-TODO
        return PagedResult(
            results=result["branches"].items(), next_page_token=end_cusrsor
        )

    def _get_after_arg(self):
        # after argument must be an empty string by default
        after = super()._get_after_arg()
        return after.encode() if after else b""

    def _get_name_include_arg(self):
        name_include = self.kwargs.get("nameInclude", None)
        return name_include.encode() if name_include else None

    def _get_index_cursor(self, index: int, node: SnapshotBranchNode):
        # Snapshot branch is using a different cursor, hence the override
        return utils.get_encoded_cursor(node.name)

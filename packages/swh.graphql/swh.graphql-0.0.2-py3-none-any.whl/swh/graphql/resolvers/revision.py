# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Union

from swh.graphql.backends import archive
from swh.graphql.utils import utils
from swh.model.swhids import CoreSWHID, ObjectType
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection
from .base_node import BaseSWHNode
from .release import BaseReleaseNode
from .snapshot_branch import SnapshotBranchNode


class BaseRevisionNode(BaseSWHNode):
    """
    Base resolver for all the revision nodes
    """

    def _get_revision_by_id(self, revision_id):
        return (archive.Archive().get_revisions([revision_id]) or None)[0]

    @property
    def parent_swhids(self):  # for ParentRevisionConnection resolver
        return [
            CoreSWHID(object_type=ObjectType.REVISION, object_id=parent_id)
            for parent_id in self._node.parents
        ]

    @property
    def directory_swhid(self):  # for RevisionDirectoryNode resolver
        return CoreSWHID(
            object_type=ObjectType.DIRECTORY, object_id=self._node.directory
        )

    @property
    def type(self):
        return self._node.type.value

    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Revision"


class RevisionNode(BaseRevisionNode):
    """
    Node resolver for a revision requested directly with its SWHID
    """

    def _get_node_data(self):
        return self._get_revision_by_id(self.kwargs.get("swhid").object_id)


class TargetRevisionNode(BaseRevisionNode):
    """
    Node resolver for a revision requested as a target
    """

    obj: Union[SnapshotBranchNode, BaseReleaseNode]

    def _get_node_data(self):
        # self.obj.target_hash is the requested revision id
        return self._get_revision_by_id(self.obj.target_hash)


class ParentRevisionConnection(BaseConnection):
    """
    Connection resolver for parent revisions in a revision
    """

    obj: BaseRevisionNode

    _node_class = BaseRevisionNode

    def _get_paged_result(self) -> PagedResult:
        # self.obj is the current(child) revision
        # self.obj.parent_swhids is the list of parent SWHIDs

        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO (pagination)
        parents = archive.Archive().get_revisions(
            [x.object_id for x in self.obj.parent_swhids]
        )
        return utils.paginated(parents, self._get_first_arg(), self._get_after_arg())


class LogRevisionConnection(BaseConnection):
    """
    Connection resolver for the log (list of revisions) in a revision
    """

    obj: BaseRevisionNode

    _node_class = BaseRevisionNode

    def _get_paged_result(self) -> PagedResult:
        # STORAGE-TODO (date in revisionlog is a dict)
        log = archive.Archive().get_revision_log([self.obj.swhid.object_id])
        # FIXME, using dummy(local) pagination, move pagination to backend
        # To remove localpagination, just drop the paginated call
        # STORAGE-TODO (pagination)
        return utils.paginated(log, self._get_first_arg(), self._get_after_arg())

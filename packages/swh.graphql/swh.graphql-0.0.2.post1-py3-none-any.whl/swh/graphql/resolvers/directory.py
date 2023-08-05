# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Union

from swh.graphql.backends import archive
from swh.model.model import Directory

from .base_node import BaseSWHNode
from .release import BaseReleaseNode
from .revision import BaseRevisionNode
from .snapshot_branch import SnapshotBranchNode


class BaseDirectoryNode(BaseSWHNode):
    """
    Base resolver for all the directory nodes
    """

    def _get_directory_by_id(self, directory_id):
        # Return a Directory model object
        # entries is initialized as empty
        # Same pattern is used in snapshot
        return Directory(id=directory_id, entries=())

    def is_type_of(self):
        return "Directory"


class DirectoryNode(BaseDirectoryNode):
    """
    Node resolver for a directory requested directly with its SWHID
    """

    def _get_node_data(self):
        directory_id = self.kwargs.get("swhid").object_id
        # path = ""
        if archive.Archive().is_directory_available([directory_id]):
            # _get_directory_by_id is not making any backend call
            # hence the is_directory_available validation
            return self._get_directory_by_id(directory_id)
        return None


class RevisionDirectoryNode(BaseDirectoryNode):
    """
    Node resolver for a directory requested from a revision
    """

    obj: BaseRevisionNode

    def _get_node_data(self):
        # self.obj.directory_swhid is the requested directory SWHID
        directory_id = self.obj.directory_swhid.object_id
        return self._get_directory_by_id(directory_id)


class TargetDirectoryNode(BaseDirectoryNode):
    """
    Node resolver for a directory requested as a target
    """

    from .directory_entry import DirectoryEntryNode

    obj: Union[SnapshotBranchNode, BaseReleaseNode, DirectoryEntryNode]

    def _get_node_data(self):
        return self._get_directory_by_id(self.obj.target_hash)

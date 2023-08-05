# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Union

from swh.graphql.backends import archive

from .base_node import BaseSWHNode
from .directory_entry import DirectoryEntryNode
from .release import BaseReleaseNode
from .snapshot_branch import SnapshotBranchNode


class BaseContentNode(BaseSWHNode):
    """
    Base resolver for all the content nodes
    """

    def _get_content_by_id(self, content_id):
        content = archive.Archive().get_content(content_id)
        return content[0] if content else None

    @property
    def checksum(self):
        # FIXME, return a Node object
        return {k: v.hex() for (k, v) in self._node.hashes().items()}

    @property
    def id(self):
        return self._node.sha1_git

    def is_type_of(self):
        # is_type_of is required only when resolving a UNION type
        # This is for ariadne to return the right type
        return "Content"


class ContentNode(BaseContentNode):
    """
    Node resolver for a content requested directly with its SWHID
    """

    def _get_node_data(self):
        return self._get_content_by_id(self.kwargs.get("swhid").object_id)


class TargetContentNode(BaseContentNode):
    """
    Node resolver for a content requested from a
    directory entry or from a release target
    """

    obj: Union[DirectoryEntryNode, BaseReleaseNode, SnapshotBranchNode]

    def _get_node_data(self):
        content_id = self.obj.target_hash
        return self._get_content_by_id(content_id)

# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.model.tests import swh_model_data


def populate_dummy_data(storage):
    for object_type, objects in swh_model_data.TEST_OBJECTS.items():
        method = getattr(storage, object_type + "_add")
        method(objects)


def get_origins():
    return swh_model_data.ORIGINS


def get_snapshots():
    return swh_model_data.SNAPSHOTS


def get_releases():
    return swh_model_data.RELEASES

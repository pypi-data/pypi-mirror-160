# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from datetime import datetime

from ariadne import ScalarType

from swh.graphql.utils import utils
from swh.model.model import TimestampWithTimezone
from swh.model.swhids import CoreSWHID

datetime_scalar = ScalarType("DateTime")
swhid_scalar = ScalarType("SWHID")
id_scalar = ScalarType("ID")


@id_scalar.serializer
def serialize_id(value):
    if type(value) is bytes:
        return value.hex()
    return value


@datetime_scalar.serializer
def serialize_datetime(value):
    # FIXME, handle error and return None
    if type(value) == TimestampWithTimezone:
        value = value.to_datetime()
    if type(value) == datetime:
        return utils.get_formatted_date(value)
    return None


@swhid_scalar.value_parser
def validate_swhid(value):
    return CoreSWHID.from_string(value)


@swhid_scalar.serializer
def serialize_swhid(value):
    return str(value)

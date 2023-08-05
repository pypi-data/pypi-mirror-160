# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import base64

import pytest

from ..data import get_releases
from .utils import get_query_response


@pytest.mark.parametrize("release", get_releases())
def test_get_release(client, release):
    query_str = (
        """
    {
      release(swhid: "%s") {
        swhid
        name {
          text
          base64
        }
        message {
          text
        }
        author {
          email {
            text
          }
          name {
            text
          }
          fullname {
            text
          }
        }
        date
        targetType
      }
    }
    """
        % release.swhid()
    )
    data, _ = get_query_response(client, query_str)

    assert data["release"] == {
        "swhid": str(release.swhid()),
        "name": {
            "text": release.name.decode(),
            "base64": base64.b64encode(release.name).decode("ascii"),
        },
        "message": {"text": release.message.decode()},
        "author": {
            "email": {"text": release.author.email.decode()},
            "name": {"text": release.author.name.decode()},
            "fullname": {"text": release.author.fullname.decode()},
        }
        if release.author
        else None,
        "date": release.date.to_datetime().isoformat() if release.date else None,
        "targetType": release.target_type.value,
    }

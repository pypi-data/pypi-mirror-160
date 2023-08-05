# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


from ariadne import graphql_sync
from flask import Flask, jsonify, request
import pytest

from swh.graphql import server as app_server
from swh.graphql.app import schema
from swh.storage import get_storage as get_swhstorage

from .data import populate_dummy_data


@pytest.fixture
def storage():
    storage = get_swhstorage(cls="memory")
    # set the global var to use the in-memory storage
    app_server.storage = storage
    # populate the in-memory storage
    populate_dummy_data(storage)
    return storage


@pytest.fixture
def test_app(storage):
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def graphql_server():
        # GraphQL queries are always sent as POST
        data = request.get_json()
        success, result = graphql_sync(
            schema, data, context_value=request, debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code

    yield app


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client

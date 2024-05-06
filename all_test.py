import json
import hashlib

import pytest
from aiohttp import web

from views import healthchecker_view, hash_view


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    app.add_routes(
        [
            web.get('/healthcheck', healthchecker_view),
            web.post('/hash', hash_view),
        ]
    )
    return event_loop.run_until_complete(aiohttp_client(app))

@pytest.mark.asyncio
async def test_healthchecker_view_success(cli):
    response = await cli.get("/healthcheck")
    body = await response.json(content_type='text/plain')

    assert response.status == 200
    assert body == {}

@pytest.mark.asyncio
async def test_healthchecker_wrong_method(cli):
    response = await cli.post("/healthcheck")

    assert response.status == 405

@pytest.mark.asyncio
async def test_hash_view_succes(cli):
    test_string = "test_string"
    expected_hash = hashlib.sha256(test_string.encode()).hexdigest()
    response = await cli.post("/hash", data=json.dumps({"string": test_string}))
    body = await response.json(content_type='text/plain')
    
    assert response.status == 200
    assert "hash_string" in body
    assert body["hash_string"] == expected_hash

@pytest.mark.asyncio
async def test_hash_view_not_string(cli):
    jsons = [
        json.dumps({"not_string": "test_not_string"}),
        json.dumps({})
    ]
    for data in jsons:
        response = await cli.post("/hash", data=data)
        body = await response.json(content_type='text/plain')

        assert response.status == 400
        assert "validation_errors" in body
import pytest

from aioviber.app import get_app


async def test_ping(test_client):
    app = get_app(bot=None)

    client = await test_client(app)
    resp = await client.get(
        '/ping',
    )
    assert resp.status == 200
    assert 'pong' == await resp.text()


async def test_static(test_client):
    app = get_app(bot=None, static_serve=True)

    client = await test_client(app)
    resp = await client.get(
        '/static/favicon.ico',
    )
    assert resp.status == 200


async def test_no_static(test_client):
    app = get_app(bot=None, static_serve=False)

    client = await test_client(app)
    resp = await client.get(
        '/static/favicon.ico',
    )
    assert resp.status == 404

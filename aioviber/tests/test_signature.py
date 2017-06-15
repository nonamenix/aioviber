import pytest
from aiohttp import web

from aioviber.app import get_app, ping
from aioviber.middleware import verify_signature, signature_middleware


def test_verify_signature():
    assert verify_signature(
        'test_message'.encode('ascii'),
        '9f29ef85c59020f5ab11d6a0937e841c0231116f91e078cc0c5e17c60509a199',
        '42f4f225c0d00988-a383ac39c65562af-3c9281ce7fd04419'
    )


class Bot:
    auth_token = '42f4f225c0d00988-a383ac39c65562af-3c9281ce7fd04419'

    def __init__(self, check_signature=True):
        self.check_signature = check_signature


async def test_middleware_good_signature(test_client):
    app = get_app(bot=Bot())
    app.router.add_post('/post', ping)

    client = await test_client(app)
    resp = await client.post(
        '/post?sig=9f29ef85c59020f5ab11d6a0937e841c0231116f91e078cc0c5e17c60509a199',
        data=b'test_message'
    )
    assert resp.status == 200
    assert 'pong' == await resp.text()


async def test_middleware_bad_signature(test_client):
    app = get_app(bot=Bot())
    app.router.add_post('/post', ping)

    client = await test_client(app)
    resp = await client.post(
        '/post?sig=BAD-SIGNATURE',
        data=b'test_message'
    )
    assert resp.status == 403


async def test_middleware_without_check(test_client):
    app = get_app(bot=Bot(check_signature=False))
    app.router.add_post('/post', ping)

    client = await test_client(app)
    resp = await client.post(
        '/post?sig=BAD-SIGNATURE',
        data=b'test_message'
    )
    assert resp.status == 200

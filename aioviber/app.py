import asyncio as aio
from aioviber.middleware import signature_middleware

from aiohttp import web


async def ping(request):
    return web.Response(text='pong')


def get_app(bot, static_serve=False) -> web.Application:
    app = web.Application(
        middlewares=[signature_middleware]
    )
    app.router.add_get('/ping', ping)
    if static_serve:
        app.router.add_static('/static', 'static')
    app.bot = bot
    return app

import logging
import asyncio as aio
import re

import aiohttp
from aiohttp import web
from viberbot import BotConfiguration
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberRequest, create_request
from urllib.parse import urlparse

from aioviber.app import get_app
from aioviber.chat import Chat
from aioviber.eventtype import EventType

from aioviber.api import Api
from aioviber.messagetype import MessageType

API_URL = "https://chatapi.viber.com/pa"
USER_AGENT = "aioviber/1.0"

__author__ = "Danil Ivanov"
__copyright__ = "Copyright 2017 Danil Ivanov"
__license__ = "MIT"

logger = logging.getLogger("aioviber")


class Bot:
    def __init__(self,
                 name: str,
                 avatar: str,
                 auth_token: str,
                 webhook: str,
                 webhook_events: list = None,
                 set_webhook_on_startup: bool = True,
                 unset_webhook_on_cleanup: bool = True,
                 host: str = '0.0.0.0',
                 port: int = 8000,
                 loop: aio.AbstractEventLoop = None,
                 check_signature: bool = True,
                 static_serve: bool = False) -> None:
        assert len(name) < 28, "Length of name should be shorty then 28 symbols"
        self.name = name
        self.avatar = avatar
        self.auth_token = auth_token

        # Server
        self.host = host
        self.port = port

        # Loop
        self.loop = aio.get_event_loop() if loop is None else loop

        # Viber API
        self._session = None
        self.api = Api(bot_configuration=BotConfiguration(
            name=self.name,
            avatar=self.avatar,
            auth_token=self.auth_token
        ), session=self.session, loop=self.loop)

        # Viber webhook
        self.webhook = webhook
        self.webhook_events = webhook_events
        self._set_webhook_on_startup = set_webhook_on_startup
        self._unset_webhook_on_cleanup = unset_webhook_on_cleanup

        def no_event_handle(event_type: str):
            return lambda msg: logger.debug("no event handle for %s", event_type)

        def no_message_handle(message_type: str):
            return lambda msg: logger.debug("no message handle for %s", message_type)

        # Callback — function for request processing messages excluded
        self._events_callbacks = {et: no_event_handle(et) for et in EventType.all()}

        # command — functions for processing text messages
        self._commands = []
        self._default_command = lambda chat: None

        # handle — functions for processing messages exclude text
        self._handlers = {mt: no_message_handle(mt) for mt in MessageType.all()}

        # Application
        self.check_signature = check_signature
        self.app = self.get_app(static_serve=static_serve)

    @property
    def session(self):
        if not self._session:
            self._session = aiohttp.ClientSession(loop=self.loop)
        return self._session

    async def set_webhook_on_startup(self):
        await aio.sleep(3)  # waiting while api will be available
        logger.info('set web hook on startup %s', self.webhook)
        self.loop.create_task(self.api.set_webhook(self.webhook, self.webhook_events))

    def get_app(self, static_serve=False) -> web.Application:
        """
        Create aiohttp application for webhook handling
        """
        app = get_app(self, static_serve=static_serve)

        # webhook handler
        webhook_path = urlparse(self.webhook).path
        app.router.add_post(webhook_path, self.webhook_handle)

        # viber webhooks registering
        if self._unset_webhook_on_cleanup:
            app.on_cleanup.append(lambda a: a.bot.api.unset_webhook())

        if self._set_webhook_on_startup:
            app.on_startup.append(lambda a: a.bot.set_webhook_on_startup())

        return app

    async def webhook_handle(self, request) -> web.Response:
        data = await request.json()
        viber_request = create_request(data)  # type: ViberRequest

        t = self.loop.create_task(self._process_request(viber_request))
        # TODO add error processing

        return web.Response()

    async def _process_request(self, request: ViberRequest) -> None:
        logger.debug('request: %s', str(request))

        coro = None

        # Process request with function from _events_callbacks
        if request.event_type in EventType.all():
            coro = self._events_callbacks[request.event_type](request)

        # Process messages
        if request.event_type == EventType.MESSAGE:
            coro = self._process_message(request)

        if coro:
            # TODO: add error processing
            t = self.loop.create_task(coro)

    async def _process_message(self, request: ViberMessageRequest) -> None:
        logger.debug('_process_message %s', request)

        if request.message._message_type == MessageType.TEXT:  # isinstance
            # Process text messages by commands
            for pattern, handler in self._commands:
                matched = re.search(pattern, str(request.message.text), re.I)
                if matched:
                    return await handler(Chat(self.api, message=request), matched)
            return await self._default_command(Chat(self.api, message=request))
        else:
            # Process other messages types with _handlers
            return await self._handlers[request.message._message_type](Chat(self.api, message=request))

    def run(self) -> None:
        web.run_app(self.app, host=self.host, port=self.port, loop=self.loop)

    def __del__(self) -> None:

        try:
            self.session.close()
        except AttributeError:
            pass

    def add_command(self, regexp, fn):
        """
        Register regexp based command for text messages processing
        """
        self._commands.append((regexp, fn))

    def default(self, coro):
        """
        Register default command for text messages processing
        """

        def decorator(coro):
            self._default_command = coro
            return coro

        return decorator

    def command(self, regexp: str):
        """
        Register a new command.
        Command — coro for text message processing.
        :param: Regular expression matching the request with text message to register
        """

        def decorator(coro):
            assert aio.iscoroutinefunction(coro), 'Decorated function should be coroutine'

            self.add_command(regexp, coro)
            return coro

        return decorator

    def add_handler(self, message_type, coro):
        self._handlers[message_type] = coro

    def message_handler(self, message_type):
        """
        Set handler for message type:
            - text
            - picture
            - contact
            - location
            - file
            - video
            - sticker
            - rich_media
            - url
        """

        def decorator(coro):
            assert aio.iscoroutinefunction(coro), 'Decorated function should be coroutine'

            self.add_handler(message_type, coro)
            return coro

        return decorator

    def event_handler(self, event_type):
        """
        Set callback for specific event type:
            - delivered
            - seen
            - conversation_started
            - message
            - subscribed
            - unsubscribed
            - failed
            - webhook
        """
        assert event_type in EventType.not_message_events(), 'Wrong event type'

        def wrap(coro):
            assert aio.iscoroutinefunction(coro), 'Decorated function should be coroutine'

            self._events_callbacks[event_type] = coro
            return coro

        return wrap

    def on_subscribed(self):
        def decorator(coro):
            assert aio.iscoroutinefunction(coro), 'function should be coroutine'

            self._events_callbacks[EventType.SUBSCRIBED] = coro
            return coro

        return decorator

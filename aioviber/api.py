import logging
from typing import List

import aiohttp
import asyncio as aio
from viberbot import BotConfiguration
from viberbot.api.consts import VIBER_BOT_API_URL, BOT_API_ENDPOINT
from viberbot.api.messages.message import Message

from aioviber.eventtype import EventType

default_headers = {
    'User-Agent': 'aioviber/1.0',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive',
}


class Api:
    endpoints = BOT_API_ENDPOINT

    def __init__(self,
                 bot_configuration: BotConfiguration,
                 session: aiohttp.ClientSession,
                 loop: aio.AbstractEventLoop):
        self._logger = logging.getLogger('aioviber.api')
        self._bot_configuration = bot_configuration
        self._viber_bot_api_url = VIBER_BOT_API_URL
        self.session = session
        self.loop = loop

    async def _make_request(self, endpoint: str, data: dict = {}):
        data['auth_token'] = self._bot_configuration.auth_token
        url = '{}/{}'.format(self._viber_bot_api_url, endpoint)
        async with self.session.post(url=url, json=data, headers=default_headers) as response:
            result = await response.json()

        if result['status'] != 0:
            error_text = "failed with result: {}".format(result)
            self._logger.error(error_text)
            raise Exception(error_text)

        return result

    async def send_message(self, to: str, message: Message) -> str:
        """ The send_message API allows PAs to send messages to Viber users
        who subscribe to the PA. Sending a message to a user will be possible
        only after the user has subscribed to the PA by pressing the subscribe
         button or by sending a message to the PA (see subscribed callback for
         additional information).

        The API supports a variety of message types: text, picture, video, file,
        location, contact and URL. Specific post data examples and required
        parameters for each message type are given below."""

        if not message.validate():
            error_text = "failed validating message: {0}".format(message)
            self._logger.error(error_text)
            raise Exception(error_text)

        data = message.to_dict()
        data.update({
            'receiver': to,
            'sender': {
                'name': self._bot_configuration.name,
                'avatar': self._bot_configuration.avatar
            }
        })
        result = await self._make_request(self.endpoints.SEND_MESSAGE, data)

        return result['message_token']

    async def set_webhook(self, url: object, webhook_events: object = None) -> object:
        """ For each set_webhook request Viber will send a callback to the
        webhook URL to confirm it is available. The expected HTTP response to
        the callback is 200 OK – any other response will mean the webhook is
         available. If the webhook is not available the set_webhook response
         sent to the user will be status 1: invalidUrl."""

        self._logger.debug(u"setting webhook to url: {0}".format(url))
        data = {
            'url': url
        }
        if webhook_events is not None:
            if isinstance(webhook_events, str):
                webhook_events = [webhook_events]

            for event in webhook_events:
                if event not in EventType.all():
                    webhook_events.remove(event)
                    self._logger.warning('Wrong event type {} in set_webhook'.format(event))

            if len(webhook_events) > 0:
                data['event_types'] = webhook_events

        result = await self._make_request(self.endpoints.SET_WEBHOOK, data)
        return result['event_types']

    async def unset_webhook(self):
        """ Once you set a webhook to your PA your 1-on-1 conversation button
        will appear and users will be able to access it.
        At the moment there is no option to disable the 1-on-1 conversation
        from the PA settings, so to disable this option you’ll need to remove
        the webhook you set for the account. Removing the webhook is done by
        Posting a set_webhook request with an empty webhook string."""

        self._logger.debug("unsetting webhook")
        return await self.set_webhook('')

    async def send_messages(self, to: str, messages: List[Message]) -> List:
        self._logger.debug("going to send messages: {0}, to: {1}".format(messages, to))

        return await aio.gather(
            *[self.send_message(to, message) for message in messages], loop=self.loop
        )

    async def get_users_status(self, ids: List[str]) -> List:
        """ The get_online request will fetch the online status of a given
        subscribed PA members. The API supports up to 100 user id per request
        and those users must be subscribed to the PA."""
        assert isinstance(ids, list), 'ids is not instance of list'
        assert len(ids) != 0, 'ids shoudn\'t be empty list'

        result = await self._make_request(self.endpoints.GET_ONLINE, {'ids': ids})
        return result['users']

    async def get_user_details(self, user_id: str):
        """ The get_user_details request will fetch the details of a specific
        Viber user based on his unique user ID. The user ID can be obtained
        from the callbacks sent to the PA regrading user’s actions. This
        request can be sent twice during a 12 hours period for each user ID."""

        assert isinstance(user_id, str), 'wrong type of user_id'
        result = await self._make_request(self.endpoints.GET_USER_DETAILS, {'id': user_id})
        return result['user']

    async def get_account_info(self):
        return await self._make_request(self.endpoints.GET_ACCOUNT_INFO)

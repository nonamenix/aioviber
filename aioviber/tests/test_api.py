from unittest.mock import Mock, MagicMock, call, ANY

import pytest
import asyncio
from asynctest import CoroutineMock

from aioviber import Api, EventType

try:
    _is_coroutine = asyncio.coroutines._is_coroutine
except AttributeError:
    _is_coroutine = True


@pytest.fixture
def user():
    return Mock


@pytest.fixture
def get_message():
    def message(valid=True):
        _message = Mock()
        _message.validate = Mock(return_value=valid)
        _message.__str__ = lambda s: 'error text'
        return _message

    return message


@pytest.fixture
def bot_configuration():
    return Mock()


@pytest.fixture
def api(bot_configuration, loop):
    api = Api(bot_configuration, session=Mock(), loop=loop)
    api._make_request = CoroutineMock(return_value=MagicMock())
    api._logger = Mock()
    return api


async def test_send_valid_message(api, user, get_message):
    message = get_message(True)
    await api.send_message(user, message)
    assert api._make_request.call_args == call('send_message', message.to_dict())


async def test_send_not_valid_message(api, user, get_message):
    message = get_message(False)

    with pytest.raises(Exception):
        await api.send_message(user, message)

    assert api._logger.error.call_args == call("failed validating message: error text")


async def test_send_messages(api, user, get_message):
    messages = [get_message() for _ in range(2)]
    await api.send_messages(user, messages)


@pytest.mark.skip
async def test_send_not_valid_messages(api, user, get_message):
    assert False


async def test_get_users_status_not_list(api):
    with pytest.raises(AssertionError):
        await api.get_users_status('some_id')


async def test_get_users_status_with_empty_list(api):
    with pytest.raises(AssertionError):
        await api.get_users_status([])


async def test_get_users_status(api):
    await api.get_users_status(['some_id'])


async def test_set_common_webhook(api):
    await api.set_webhook(url='http://example.com')
    assert api._make_request.call_args == call('set_webhook', {'url': 'http://example.com'})


async def test_set_webhook_with_events_list(api):
    await api.set_webhook(url='http://example.com', webhook_events=[EventType.SUBSCRIBED])
    assert api._make_request.call_args == call(
        'set_webhook', {'url': 'http://example.com', 'event_types': ['subscribed']}
    )


async def test_set_webhook_with_event_str(api):
    await api.set_webhook(url='http://example.com', webhook_events=EventType.SUBSCRIBED)
    assert api._make_request.call_args == call(
        'set_webhook', {'url': 'http://example.com', 'event_types': ['subscribed']}
    )


async def test_set_webhook_with_not_valid_event(api):
    await api.set_webhook(url='http://example.com', webhook_events=['WRONG'])
    assert api._logger.warning.call_args == call('Wrong event type WRONG in set_webhook')
    assert api._make_request.call_args == call('set_webhook', {'url': 'http://example.com'})


async def test_unset_webhook(api):
    await api.unset_webhook()
    assert api._make_request.call_args == call('set_webhook', {'url': ''})


async def test_get_user_details(api):
    await api.get_user_details('user_id')
    assert api._make_request.call_args == call('get_user_details', {'id': 'user_id'})


async def test_get_account_info(api):
    await api.get_account_info()
    assert api._make_request.call_args == call('get_account_info')

#
# class CoroutineContextManager(CoroutineMock):
#     async def __aexit__(self, *args, **kwargs):
#         pass
#
#     async def __aenter__(self, *args, **kwargs):
#         return Mock()
#
#
# async def test_make_request(bot_configuration, loop):
#     api = Api(bot_configuration, CoroutineContextManager(), loop)
#     api._logger = Mock()
#     await api._make_request(api.endpoints.SEND_MESSAGE)

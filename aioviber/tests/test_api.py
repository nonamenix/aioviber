from unittest.mock import Mock, MagicMock, call, ANY

import pytest
from asynctest import CoroutineMock

from aioviber import Api


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
    session = Mock()

    api = Api(bot_configuration, session, loop)
    api._make_request = CoroutineMock(return_value=MagicMock())
    api._logger = Mock()

    return api


async def test_send_valid_message(api, user, get_message):
    message = get_message(True)
    await api.send_message(user, message)

    # api._make_request.assert_any_call('send_message', ANY, ANY)
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

from unittest.mock import Mock

import pytest

from viberbot.api.viber_requests import ViberMessageRequest

from aioviber import Chat


@pytest.fixture()
def api():
    return Mock()


@pytest.fixture()
def user():
    return Mock()


@pytest.fixture()
def message():
    return Mock()


@pytest.fixture()
def chat(api, user):
    return Chat(api, sender=user)


# http://www.voidspace.org.uk/python/mock/patch.html#patch-multiple
def test_not_enough_arguments_init(api):
    with pytest.raises(TypeError):
        Chat()

    with pytest.raises(AssertionError):
        Chat(api=api)


def test_message_specified(api, user):
    request = ViberMessageRequest()
    request._sender = user
    chat = Chat(api, request)
    assert chat.sender == user


def test_sender_specified(api, user):
    chat = Chat(api, sender=user)
    assert chat.sender == user


def test_send_text(chat, message):
    chat.send_text(message)
    assert chat.api.send_message.called


def test_send_message(chat, message):
    chat.send_message(message)
    assert chat.api.send_message.called


def test_send_messages(chat, message):
    chat.send_messages([message])
    assert chat.api.send_messages.called


def test_send_sticker(chat, message):
    chat.send_sticker(message)
    assert chat.api.send_message.called


def test_send_contact(chat):
    with pytest.raises(TypeError):
        chat.send_contact()

    chat.send_contact(name='name', phone_number='phone_number')
    assert chat.api.send_message.called


def test_send_location(chat):
    with pytest.raises(TypeError):
        chat.send_location()

    chat.send_location(0, 0)
    assert chat.api.send_message.called


def test_send_video(chat):
    with pytest.raises(TypeError):
        chat.send_video()
        chat.send_video(media='http://example.com/test.mp4')

    chat.send_video(media='http://example.com/test.mp4', size=100)
    assert chat.api.send_message.called


def test_send_url(chat):
    with pytest.raises(TypeError):
        chat.send_url()

    chat.send_url(url="http://example.com")
    assert chat.api.send_message.called


def test_send_rich_media(chat):
    with pytest.raises(TypeError):
        chat.send_rich_media()

    chat.send_rich_media(rich_media=Mock())
    assert chat.api.send_message.called

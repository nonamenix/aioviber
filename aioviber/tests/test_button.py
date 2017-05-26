from urllib.parse import urlparse
import pytest

from aioviber.keyboard import Button, ActionType


def test_no_arguments():
    with pytest.raises(TypeError):
        Button()


def test_not_enough_arguments():
    with pytest.raises(AssertionError):
        Button('command')


def test_success_creation():
    Button('command', text='http://example.com/image.jpg')
    Button('command', bg_media='http://example.com/image.jpg')
    Button('command', image='http://example.com/image.jpg')
    Button('command', bg_color='#ffffff')


def test_default_utm():
    body = 'http://example.com/'
    default_utm = ['utm_campaign=viber', 'utm_medium=link', 'utm_source=social-networks']
    btn = Button('http://example.com/', text="External link", action_type=ActionType.open_url)
    assert btn.action_body == '{}{}'.format(body, default_utm)


def test_default_utm_action_with_get_params():
    body = 'http://example.com/?v=1'
    default_utm = '?utm_campaign=viber&utm_medium=link&utm_source=social-networks'
    btn = Button('http://example.com/', text="External link", action_type=ActionType.open_url)
    assert btn.action_body == '{}{}'.format(body, default_utm)

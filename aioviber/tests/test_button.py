from urllib.parse import urlparse
import pytest

from aioviber.keyboard import Button, ActionType, TextHorizontalAlign, TextVerticalAlign, TextSize, ExternalLinkButton


def test_no_arguments():
    with pytest.raises(TypeError):
        Button()


def test_not_enough_arguments():
    with pytest.raises(AssertionError):
        Button('command')


@pytest.mark.parametrize('second_arg', [
    {'text': 'http://example.com/image.jpg'},
    {'bg_media': 'http://example.com/image.jpg'},
    {'image': 'http://example.com/image.jpg'},
    {'bg_color': '#ffffff'},
], ids=['text', 'bg_media', 'image', 'bg_color'])
def test_success_creation(second_arg):
    Button('command', **second_arg)


@pytest.mark.parametrize('link', [
    'http://example.com/',
])
def test_default_utm(link):
    default_utm = ['utm_campaign=viber', 'utm_medium=link', 'utm_source=social-networks']
    btn = Button(link, text="External link", action_type=ActionType.open_url)

    for param in default_utm:
        assert param in btn.action_body


def test_to_dict():
    assert Button('action', text='Action').to_dict() == {
        'ActionBody': 'action',
        'Columns': 6, 'Rows': 1,
        'Text': 'Action'
    }


def test_customized_button_to_dict():
    assert Button(
        'actionbody',
        text='Link',
        action_type=ActionType.none,
        silent=True,
        image='http://example.com/image.jpg',
        text_v_align=TextVerticalAlign.bottom,
        text_h_align=TextHorizontalAlign.center,
        text_size=TextSize.large,
        text_opacity=80,
        bg_media='http://example.com/image.jpg',
        bg_color='#ffffff',
        bg_loop=False
    ).to_dict() == {
               'ActionBody': 'actionbody',
               'ActionType': 'none',
               'BgColor': '#ffffff',
               'BgLoop': False,
               'BgMedia': 'http://example.com/image.jpg',
               'Columns': 6,
               'Image': 'http://example.com/image.jpg',
               'Rows': 1,
               'Silent': True,
               'Text': 'Link',
               'TextHAlign': 'center',
               'TextOpacity': 80,
               'TextSize': 'large',
               'TextVAlign': 'bottom'
           }


def test_external_link_creation():
    btn = ExternalLinkButton('http://example.com', 'example.com', _utm='')
    assert btn.text == 'example.com'
    assert btn.action_body == 'http://example.com'


def test_bad_external_link_creation():
    with pytest.raises(TypeError):
        assert ExternalLinkButton('http://example.com')

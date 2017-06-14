import pytest

from aioviber import Keyboard, Button


def test_not_enough_arguments():
    with pytest.raises(TypeError):
        Keyboard()


def test_creation():
    keyboard = Keyboard(buttons=[
        Button('test', text='test')
    ])


def test_add_button():
    keyboard = Keyboard(buttons=[
        Button('test', text='test')
    ])

    keyboard.add_button(Button('test', text='test'))
    assert len(keyboard._buttons) == 2


def test_to_dict():
    keyboard = Keyboard(buttons=[
        Button('test', text='test')
    ])

    assert keyboard.to_dict() == {
        'Buttons': [{'ActionBody': 'test', 'Columns': 6, 'Rows': 1, 'Text': 'test'}],
        'Type': 'keyboard'}


def test_to_dict_with_bg_and_height():
    keyboard = Keyboard(bg_color='#ffffff', default_height=True, buttons=[
        Button('test', text='test'),
    ])

    assert keyboard.to_dict() == {
        'Buttons': [{'ActionBody': 'test', 'Columns': 6, 'Rows': 1, 'Text': 'test'}],
        'Type': 'keyboard',
        'BgColor': '#ffffff',
        'DefaultHeight': True
    }

import pytest

from aioviber import Carousel, Button


def test_failed_creation():
    with pytest.raises(AssertionError):
        Carousel()


def test_creation():
    Carousel(buttons=[
        Button('test', text='test')
    ])


def test_to_dict():
    carousel = Carousel(buttons=[
        Button('test', text='test')
    ])

    assert carousel.to_dict() == {
        'Buttons': [{'ActionBody': 'test', 'Columns': 6, 'Rows': 1, 'Text': 'test'}],
        'ButtonsGroupColumns': 6,
        'ButtonsGroupRows': 6
    }

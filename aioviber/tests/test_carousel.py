import pytest

from aioviber import Carousel


def test_failed_creation():
    with pytest.raises(AssertionError):
        Carousel()


def test_creation():
    Carousel()

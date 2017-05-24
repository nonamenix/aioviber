import pytest

from aioviber import Bot


@pytest.fixture
def bot_params(loop):
    return dict(
        name='test',
        avatar='http://example.com/avatar.jpg',
        auth_token='test-token',
        webhook='https://example.com/webhook',
        loop=loop,
        set_webhook_on_startup=False,
        unset_webhook_on_cleanup=False
    )


def test_success_creation(bot_params):
    Bot(**bot_params)


def test_long_name(bot_params):
    with pytest.raises(AssertionError):
        bot_params['name'] = 'a' * 29
        Bot(**bot_params)

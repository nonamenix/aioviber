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


@pytest.fixture
def bot(bot_params):
    return Bot(**bot_params)


def test_bad_initial():
    with pytest.raises(TypeError):
        Bot()


def test_success_creation(bot_params):
    Bot(**bot_params)


def test_long_name(bot_params):
    with pytest.raises(AssertionError):
        bot_params['name'] = 'a' * 29
        Bot(**bot_params)


def test_success_command(bot):
    @bot.command('ping')
    async def ping(chat, matched):
        await chat.send_text('pong')


def test_command_should_be_coroutine(bot):
    with pytest.raises(AssertionError):
        @bot.command('ping')
        def ping(chat, matched):
            pass


def test_default_command(bot):
    @bot.default
    def default(chat):
        pass

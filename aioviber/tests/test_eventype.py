from aioviber import EventType


def test_all():
    assert EventType.all() == [
        'seen',
        'conversation_started',
        'delivered',
        'message',
        'subscribed',
        'unsubscribed',
        'failed',
        'webhook'
    ]


def test_message_excluded():
    assert EventType.not_message_events() == [
        'seen',
        'conversation_started',
        'delivered',
        'subscribed',
        'unsubscribed',
        'failed',
        'webhook'
    ]


def test_update_statuses():
    assert EventType.message_status_update() == ['delivered', 'failed', 'seen']


def test_subscriptions():
    assert EventType.subscriptions() == ['subscribed', 'unsubscribed']


def test_chat():
    assert EventType.chat() == ['conversation_started', 'message', 'subscribed']

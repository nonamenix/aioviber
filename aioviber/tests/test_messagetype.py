from aioviber import MessageType


def test_messages_all():
    assert MessageType.all() == ['text',
                                 'rich_media',
                                 'sticker',
                                 'url',
                                 'location',
                                 'contact',
                                 'file',
                                 'picture',
                                 'video']


def test_messages_text():
    assert MessageType.text() == ['text', 'url']

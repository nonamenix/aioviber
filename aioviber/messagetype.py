from typing import List

from viberbot.api.messages import MessageType as BaseMessageType


class MessageType(BaseMessageType):
    @classmethod
    def all(cls) -> List[str]:
        return [
            cls.TEXT, cls.RICH_MEDIA, cls.STICKER, cls.URL, cls.LOCATION, cls.CONTACT, cls.FILE, cls.PICTURE, cls.VIDEO
        ]

    @classmethod
    def text(cls) -> List[str]:
        return [
            cls.TEXT, cls.URL
        ]

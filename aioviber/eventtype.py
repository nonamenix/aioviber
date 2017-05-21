from typing import List

from viberbot.api.event_type import EventType as BaseEventType


class EventType(BaseEventType):
    @classmethod
    def all(cls) -> List[str]:
        return [
            cls.SEEN, cls.CONVERSATION_STARTED, cls.DELIVERED, cls.MESSAGE,
            cls.SUBSCRIBED, cls.UNSUBSCRIBED, cls.FAILED, cls.WEBHOOK
        ]

    @classmethod
    def not_message_events(cls) -> List[str]:
        return [
            cls.SEEN, cls.CONVERSATION_STARTED, cls.DELIVERED, cls.SUBSCRIBED,
            cls.UNSUBSCRIBED, cls.FAILED, cls.WEBHOOK
        ]

    @classmethod
    def message_status_update(cls) -> List[str]:
        return [cls.DELIVERED, cls.FAILED, cls.SEEN]

    @classmethod
    def subscriptions(cls) -> List[str]:
        return [cls.SUBSCRIBED, cls.UNSUBSCRIBED]

    @classmethod
    def chat(cls) -> List[str]:
        return [cls.CONVERSATION_STARTED, cls.MESSAGE, cls.SUBSCRIBED]

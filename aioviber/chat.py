from typing import List

from viberbot.api.messages import TextMessage, StickerMessage, ContactMessage, LocationMessage, VideoMessage, \
    URLMessage, RichMediaMessage
from viberbot.api.messages.data_types.contact import Contact
from viberbot.api.messages.data_types.location import Location
from viberbot.api.messages.message import Message
from viberbot.api.user_profile import UserProfile
from viberbot.api.viber_requests import ViberMessageRequest

from aioviber.api import Api
from aioviber.keyboard import Keyboard, Carousel


class Chat:
    def __init__(self, api: Api, message: ViberMessageRequest = None, sender: UserProfile = None):
        assert message or sender, 'Specify message or sender'

        self.api = api
        self.message = message
        self._sender = sender

    @property
    def sender(self):
        sender = self._sender
        try:
            sender = self.message.sender
        except AttributeError:
            pass
        return sender

    def send_messages(self, messages: List[Message]):
        return self.api.send_messages(
            to=self.sender.id,
            messages=messages
        )

    def send_message(self, message: Message):
        return self.api.send_message(
            to=self.sender.id,
            message=message
        )

    def send_text(self, text: str, keyboard: Keyboard = None, min_api_version=None, tracking_data: str = None):
        return self.api.send_message(
            to=self.sender.id,
            message=TextMessage(
                text=text,
                keyboard=keyboard.to_dict() if keyboard else None,
                min_api_version=min_api_version,
                tracking_data=tracking_data
            ))

    def send_sticker(self, sticker_id: int, keyboard: Keyboard = None, min_api_version=None, tracking_data: str = None):
        return self.api.send_message(
            to=self.sender.id,
            message=StickerMessage(
                sticker_id=sticker_id,
                keyboard=keyboard.to_dict() if keyboard else None,
                min_api_version=min_api_version,
                tracking_data=tracking_data
            )
        )

    def send_contact(self, name: str, phone_number: str, avatar: str = None, keyboard: Keyboard = None,
                     min_api_version=None, tracking_data: str = None):
        return self.api.send_message(
            to=self.sender.id,
            message=ContactMessage(
                contact=Contact(name=name, phone_number=phone_number, avatar=avatar),
                keyboard=keyboard.to_dict() if keyboard else None,
                min_api_version=min_api_version,
                tracking_data=tracking_data
            )
        )

    def send_location(
            self,
            lat: float,
            lon: float,
            keyboard: Keyboard = None,
            min_api_version=None,
            tracking_data: str = None):
        return self.api.send_message(
            to=self.sender.id,
            message=LocationMessage(
                location=Location(lat, lon),
                keyboard=keyboard.to_dict() if keyboard else None,
                min_api_version=min_api_version,
                tracking_data=tracking_data
            )
        )

    def send_video(
            self,
            media: str,
            size: int,
            thumbnail: str = None,
            duration: int = None,
            text: str = None,
            keyboard: Keyboard = None,
            min_api_version=None,
            tracking_data: str = None):
        return self.api.send_message(
            to=self.sender.id,
            message=VideoMessage(
                media=media,
                size=size,
                thumbnail=thumbnail,
                duration=duration,
                text=text,
                keyboard=keyboard.to_dict() if keyboard else None,
                min_api_version=min_api_version,
                tracking_data=tracking_data
            )
        )

    def send_url(
            self,
            url: str,
            keyboard: Keyboard = None,
            min_api_version=None,
            tracking_data: str = None):
        return self.api.send_message(
            to=self.sender.id,
            message=URLMessage(
                media=url,
                keyboard=keyboard.to_dict() if keyboard else None,
                min_api_version=min_api_version,
                tracking_data=tracking_data
            )
        )

    def send_rich_media(
            self,
            rich_media: Carousel,
            keyboard: Keyboard = None,
            min_api_version: int = 2,
            tracking_data: str = None):
        return self.api.send_message(
            to=self.sender.id,
            message=RichMediaMessage(
                rich_media=rich_media.to_dict(),
                keyboard=keyboard.to_dict() if keyboard else None,
                min_api_version=min_api_version,
                tracking_data=tracking_data
            )
        )

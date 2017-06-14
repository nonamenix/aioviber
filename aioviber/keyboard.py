from typing import List

from aioviber.utils import snake_case_2_camel_case, add_url_params

DEFAULT_UTM = {
    'utm_campaign': 'viber',
    'utm_medium': 'link',
    'utm_source': 'social-networks'
}


class DefaultEnum:
    @classmethod
    def is_default(cls, choice):
        return choice == cls._default or choice is None


class BgMediaType(DefaultEnum):
    picture = 'picture'
    gif = 'gif'

    all = (picture, gif)
    _default = picture


class TextVerticalAlign(DefaultEnum):
    top = 'top'
    middle = 'middle'
    bottom = 'bottom'

    all = (top, middle, bottom)
    _default = middle


class TextHorizontalAlign(DefaultEnum):
    left = 'left'
    center = 'center'
    right = 'right'

    all = (left, center, right)
    _default = center


class TextSize(DefaultEnum):
    small = 'small'
    regular = 'regular'
    large = 'large'

    all = (small, regular, large)
    _default = regular


class ActionType(DefaultEnum):
    reply = 'reply'
    open_url = 'open-url'
    none = 'none'

    all = (reply, open_url, none)
    _default = reply


class MediaType(DefaultEnum):
    picture = 'picture'
    gif = 'gif'

    all = (picture, gif)
    _default = picture


class Button:
    def __init__(
            self,
            action_body: str,
            columns: int = 6,
            rows: int = 1,
            silent: bool = None,
            image: str = None,
            text: str = None,
            action_type: str = None,
            text_v_align: str = None,
            text_h_align: str = None,
            text_size: str = None,
            text_opacity: int = None,
            bg_media: str = None,
            bg_color: str = None,
            bg_media_type: str = None,
            bg_loop: bool = None,
            _utm: dict = DEFAULT_UTM
    ):
        """
        :param action_body: ext for reply and none. ActionType or URL for open-url.
            See reply logic for more details. For ActionType reply - text For
            ActionType open-url - Valid URL. Max length: 250 characters
        :param action_type: Type of action pressing the button will perform.
            Reply - will send a reply to the PA. open-url - will open the
            specified URL and send the URL as reply to the PA. See reply
            logic for more details. https://viber.github.io/docs/tools/keyboards/#replyLogic
        :param columns: Button width in columns. Allowed 1-6 See keyboard
            design for more details https://viber.github.io/docs/tools/keyboards/#keyboardDesign
        :param rows: Button height in rows. Allowed 1-2. See keyboard design
            for more details https://viber.github.io/docs/tools/keyboards/#keyboardDesign
        :param silent: Determine whether the user action is presented in the
            conversation
        :param bg_color: Background color of button. Valid color HEX value
        :param bg_media:  URL for background media content (picture or gif). Will be
            placed with aspect to fill logic
        :param bg_media_type: picture, gif. For picture - JPEG and PNG files are
            supported. Max size: 500 kb
        :param bg_loop: When true - animated background media (gif) will loop
            continuously. When false - animated background media will play
            once and stop
        :param image: URL of image to place on top of background (if any). Can
            be a partially transparent image that will allow showing some of
            the background. Will be placed with aspect to fill logic
        :param text: Text to be displayed on the button. Can contain some HTML
            tags - see keyboard design for more details
        :param text_v_align: Vertical alignment of the text.
            Valid values: top, middle, bottom
        :param text_h_align: Horizontal align of the text.
        :param text_opacity: Text opacity 0-100
        """
        assert text or bg_media or image or bg_color, \
            "Button should have at least one of the following: text, bg_media, image, bg_color"

        self.action_body = action_body
        self.action_type = action_type

        assert columns is None or (0 < columns <= 6), 'columns possible values 1-6'
        self.columns = columns

        # assert columns is None or (0 < rows <= 2), 'rows possible values 1-2'
        self.rows = rows

        assert text_opacity is None or (0 < text_opacity <= 100), 'text opacity possible values 1-100'
        self.text_opacity = text_opacity

        self.silent = silent
        self.image = image
        self.text = text
        self.text_v_align = text_v_align
        self.text_h_align = text_h_align
        self.text_size = text_size

        # Background
        self.bg_media = bg_media
        self.bg_media_type = bg_media_type
        self.bg_loop = bg_loop
        self.bg_color = bg_color

        # Append utm
        self._utm = _utm
        if self.action_type == ActionType.open_url:
            self.action_body = add_url_params(self.action_body, self._utm)

    def to_dict(self) -> dict:
        d = {}

        mapping = {field: snake_case_2_camel_case(field) for field in Button.__init__.__annotations__.keys() if
                   not field.startswith('_')}
        for field_name, api_name in mapping.items():
            value = getattr(self, field_name)
            if value is not None:
                d[api_name] = value

        return d


class ExternalLinkButton(Button):
    def __init__(self, url: str, text: str, action_type=ActionType.open_url, **kwargs):
        super(ExternalLinkButton, self).__init__(
            action_body=url,
            text=text,
            action_type=action_type,
            **kwargs)


class Keyboard:
    def __init__(self, buttons: List[Button], default_height: bool = None, bg_color: str = None):

        """
        The public accounts API allows sending a custom keyboard with each
        messsage, to supply the user with a set of predefined replies or
        actions. The keyboard can be attached to any message type or sent on
        it’s on. Once received, the keyboard will appear to the user instead
        of the device’s native keyboard. The keyboards are fully customizable
        and can be created and designed specifically for the PA’s needs.

        See more https://viber.github.io/docs/tools/keyboards/#keyboards

        :param default_height: When true - the keyboard will always be
            displayed with the same height as the native keyboard.When false -
            short keyboards will be displayed with the minimal possible height.
            Maximal height will be native keyboard height.
        :param bg_color: Background color of the keyboard. Valid color HEX value
        :param buttons: Array containing all keyboard buttons by order.
        """
        self.default_height = default_height
        self._buttons = buttons.copy()
        self.bg_color = bg_color

    def add_button(self, button: Button) -> None:
        self._buttons.append(button)

    def to_dict(self) -> dict:
        d = {
            "Type": "keyboard",
            "Buttons": [button.to_dict() for button in self._buttons]
        }

        if self.bg_color:
            d['BgColor'] = self.bg_color
        if self.default_height:
            d["DefaultHeight"] = self.default_height

        return d


class Carousel:
    """
    The Carousel Content Message type allows a user to scroll through a list of
    items, each composed of an image, description and call to action button. 
    Use Carousel with Rich Media Messages.
    
    :param alt_text: Backward compatibility text, limited to 7,000 characters	 
    :param buttons_group_columns: Number of columns per carousel content block.
        Default 6 columns 1 - 6
    :param buttons_group_rows: Number of rows per carousel content block. 
        Default 7 rows 1 - 7
    :param buttons: Array of buttons. Max of 6 * ButtonsGroupColumns * ButtonsGroupRows
    """

    def __init__(
            self,
            buttons_group_columns: int = 6,  # ButtonsGroupColumns
            buttons_group_rows: int = 6,  # ButtonsGroupRows
            buttons: List[Button] = []
    ):
        assert 0 < buttons_group_rows <= 7, 'Possible values for buttons group rows 1 - 7'
        self.buttons_group_rows = buttons_group_rows

        assert 0 < buttons_group_columns <= 6, 'Possible values for buttons group columns 1 - 6'
        self.buttons_group_columns = buttons_group_columns

        assert buttons != [], 'Carousel should have buttons'
        self._buttons = buttons

    def to_dict(self) -> dict:
        return {
            'ButtonsGroupColumns': self.buttons_group_columns,
            'ButtonsGroupRows': self.buttons_group_rows,
            "Buttons": [button.to_dict() for button in self._buttons]
        }

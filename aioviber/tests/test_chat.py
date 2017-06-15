import pytest

# @pytest.fixture
# def api():
#     class API:
#         def send_message(self, to, message=None, messages=None):
#             pass
#
#     return API()
from aioviber import Chat


def test_init():
    # http://www.voidspace.org.uk/python/mock/patch.html#patch-multiple
    chat = Chat()

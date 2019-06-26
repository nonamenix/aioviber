aioviber
--------

Asynchronous Python API for building Viber bots.

|Build Status| |Coverage Status| |Package version| |Python versions|

Example
=======

.. code:: python

    import logging

    from aioviber.bot import Bot
    from aioviber.chat import Chat
    from viberbot.api.viber_requests import ViberSubscribedRequest

    logger = logging.getLogger(__name__)

    bot = Bot(
        name='ViberBot',
        avatar='http://avatar.example.com/avatar.jpg',
        auth_token="**************-**************-**************",  # Public account auth token
        host="my.host.com",  # should be available from wide area network
        port=80,
        webhook="https://my.host.com",  # Webhook url
    )

    @bot.command('ping')
    async def ping(chat: Chat, matched):
        await chat.send_text('pong')

    @bot.event_handler('subscribed')
    async def user_subscribed(chat: Chat, request: ViberSubscribedRequest):
        await chat.send_text('Welcome')

    @bot.message_handler('sticker')
    async def sticker(chat: Chat):
        await chat.send_sticker(5900)

    if __name__ == '__main__':  # pragma: no branch
        bot.run()  # pragma: no cover

API designed similar to `aiotg`_

Getting Started
===============

In order to implement the API you will need the following: 1. An Active
Viber account on a platform which supports PA (iOS/Android). 2. Active
Public Account; 3. Public Account authentication token; 4. Write your
bot with **aioviber**.

Read more: `Public Account Documentation — Viber REST API`_

There is no way to run viber bot in polling mode like Telegram.

Install
=======

::

    pip install aioviber
    

Local testing
=============

For testing your bot from local machine use ngrok. Read more https://github.com/nonamenix/aioviber/issues/1#issuecomment-504766258

Viber API
=========

Messaging flow
--------------

.. figure:: https://developers.viber.com/docs/img/send_and_receive_message_flow.png
   :alt: Messaging flow

   Messaging flow

Events types
------------

Documentation about events types
https://developers.viber.com/docs/api/rest-bot-api/#callbacks

Callbacks can be proceeded with ``@bot.event_handler('subscribed')``
decorator

-  `Subscribed`_
-  `Unsubscribed`_
-  `Conversation started`_
-  `Sending a welcome message`_
-  `Message receipts callbacks`_
-  `Failed callback`_
-  `Receive message from user`_

.. _aiotg: https://github.com/szastupov/aiotg
.. _Public Account Documentation — Viber REST API: https://developers.viber.com/docs/api/rest-bot-api/#getting-started
.. _Subscribed: https://developers.viber.com/docs/api/rest-bot-api/#subscribed
.. _Unsubscribed: https://developers.viber.com/docs/api/rest-bot-api/#unsubscribed
.. _Conversation started: https://developers.viber.com/docs/api/rest-bot-api/#conversation-started
.. _Sending a welcome message: https://developers.viber.com/docs/api/rest-bot-api/#welcome-message-flow
.. _Message receipts callbacks: https://developers.viber.com/docs/api/rest-bot-api/#message-receipts-callbacks
.. _Failed callback: https://developers.viber.com/docs/api/rest-bot-api/#failed-callback
.. _Receive message from user: https://developers.viber.com/docs/api/rest-bot-api/#receive

.. |Build Status| image:: https://api.travis-ci.org/nonamenix/aioviber.svg
   :target: https://travis-ci.org/nonamenix/aioviber
.. |Coverage Status| image:: https://coveralls.io/repos/github/nonamenix/aioviber/badge.svg
   :target: https://coveralls.io/github/nonamenix/aioviber
.. |Package version| image:: https://badge.fury.io/py/aioviber.svg
   :target: https://pypi.python.org/pypi/aioviber
.. |Python versions| image:: https://img.shields.io/badge/python-3.5%2C%203.6%2C%203.7-blue.svg
   :target: https://www.python.org/doc/versions/

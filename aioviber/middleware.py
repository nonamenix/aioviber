import hmac
import hashlib

import logging
from aiohttp import web
from aiohttp.web_request import Request

logger = logging.getLogger(__name__)


def calculate_message_signature(message, auth_token):
    return hmac.new(
        bytes(auth_token.encode('ascii')),
        msg=message,
        digestmod=hashlib.sha256).hexdigest()


def verify_signature(request_data, signature, auth_token):
    return signature == calculate_message_signature(request_data, auth_token)


async def signature_middleware(app, handler):
    """Check request signature"""

    async def middleware_handler(request: Request):
        if request.method == 'POST' and app.bot.check_signature:
            sig = request.query.get('sig')
            body = await request.read()
            if verify_signature(body, sig, app.bot.auth_token):
                response = await handler(request)
            else:
                logger.warning('Post requests with bad signature {sig} {body}'.format(
                    sig=sig, body=body
                ))
                response = web.HTTPForbidden()
        else:
            response = await handler(request)

        return response

    return middleware_handler

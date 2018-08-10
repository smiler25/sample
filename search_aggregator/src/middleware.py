from aiohttp import web
from logging import getLogger

logger = getLogger(__name__)


async def handle_400(request, msg=None):
    return web.json_response({'error': 'Bad request', 'message': msg}, status=400)


async def handle_404(request, *args):
    return web.json_response({'error': 'Not found'}, status=404)


async def handle_500(request, msg=None):
    return web.json_response({'error': 'Internal server error', 'message': msg}, status=500)


def create_error_middleware(status_handlers):
    @web.middleware
    async def response_middleware(request, handler):
        try:
            response = await handler(request)
            override = status_handlers.get(response.status)
            if override:
                return await override(request)
            return response

        except web.HTTPException as e:
            logger.error('web.HTTPException {}'.format(repr(e)), exc_info=True)
            override = status_handlers.get(e.status)
            if override:
                return await override(request)
            raise
        except AssertionError as e:
            logger.error('AssertionError {}'.format(repr(e)), exc_info=True)
            override = status_handlers.get(400)
            if override:
                return await override(request, e.args[0] if e.args else None)
            raise
        except Exception as e:
            logger.error('Exception {}'.format(repr(e)), exc_info=True)
            override = status_handlers.get(500)
            if override:
                return await override(request, e.args[0] if e.args else None)
            raise

    return response_middleware


def setup_middlewares(app):
    response_middleware = create_error_middleware({
        400: handle_400,
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(response_middleware)

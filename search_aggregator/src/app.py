from aiohttp import web
from src.routes import setup_routes
from src.middleware import setup_middlewares


async def init_app():
    app = web.Application()
    setup_routes(app)
    setup_middlewares(app)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), host='127.0.0.1')

import asyncio
from aiohttp import web
from aiohttp_graphql import GraphQLView
from graphql.execution.executors.asyncio import AsyncioExecutor

from .controllers import search
from .views import schema

def setup_routes(app):
    app.add_routes([
        web.get('/search', search),
    ])
    GraphQLView.attach(app, schema=schema, route_path='/graphql',
                       executor=AsyncioExecutor(asyncio.get_event_loop()))

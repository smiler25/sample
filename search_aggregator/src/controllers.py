from aiohttp import web
from .models import SearchEngine


async def handle_request(request):
    query = request.query
    data = {'query': query.get('query')}
    if not data['query']:
        raise AssertionError('Query not specified')
    data['limit'] = query.get('limit', None)
    return data


async def search(request):
    data = await handle_request(request)
    res = await SearchEngine.search_all(data['query'], data['limit'])
    return web.json_response(res)

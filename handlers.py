from aiohttp import web
from meepo.core import get, post


@get('/')
def index(a, request):
    print(request)
    return web.Response(body=b'<h1>Awesome</h1>')

@post('/')
def index(a, request):
    print(request)
    return web.Response(body=b'<h1>Awesome</h1>')

@get('/blog/{id}')
def get_blog(id):
    return web.Response(body=b'<h1>get_blog</h1>')

@get('/ggg')
def get_ggg(request, *, name):
    print(request)
    return web.Response(body=b'<h1>get_blog</h1>')

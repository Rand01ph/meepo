#! /usr/bin/env python
# coding=utf-8
# author: Rand01ph

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os

from aiohttp import web

from meepo.core import add_route, get

@get('/')
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')

@get('/aaa')
def aaa(*args):
    return web.Response(body=b'<h1>aaa</h1>')

@get('/blog/{id}')
def get_blog(id):
    return web.Response(body=b'<h1>get_blog</h1>')

@get('/ggg')
def get_ggg(a, b, *, c, d=10):
    return web.Response(body=b'<h1>get_blog</h1>')

async def init(loop):
    app = web.Application(loop=loop)
    add_route(app, index)
    add_route(app, aaa)
    add_route(app, get_ggg)
    add_route(app, get_blog)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9999)
    logging.info('server started at http://127.0.0.1:999...')
    return srv

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

if __name__ == '__main__':
    main()

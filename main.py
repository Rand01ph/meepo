#! /usr/bin/env python
# coding=utf-8
# author: Rand01ph

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os

from aiohttp import web

from meepo.core import add_routes

async def init(loop):
    app = web.Application(loop=loop)
    add_routes(app, 'handlers')
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9999)
    logging.info('server started at http://127.0.0.1:999...')
    return srv

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

if __name__ == '__main__':
    main()

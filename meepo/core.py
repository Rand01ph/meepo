#! /usr/bin/env python3
# coding=utf-8
# author: Rand01ph

import functools, asyncio, inspect

from aiohttp import web

def get(path):
    '''
    @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator


def post(path):
    '''
    @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn

    async def __call__(self, request):
        kw = None
        r = await self._func(**kw)
        return r


def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__routh__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not define in %s.', str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    app.router.add_route(method, path, RequestHandler(app, fn))

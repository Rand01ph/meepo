#! /usr/bin/env python3
# coding=utf-8
# author: Rand01ph

import functools, asyncio, inspect

from urllib import parse

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
        self._params = inspect.signature(fn).parameters

    async def __call__(self, request):
        kw = None
        func_items = self._params.items()
        func_args = [name for name, param in func_items]
        required_kw_args = [name for name, param in func_items
                            if param.kind == param.KEYWORD_ONLY
                            and param.default == inspect.Parameter.empty]
        named_kw_args = [name for name, param in func_items
                            if param.kind == param.KEYWORD_ONLY]
        if not func_items:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest("JSON body must be object.")
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            kw = dict(**request.match_info)
        if 'request' in func_args:
            kw['request'] = request
        print('call with args: %s' % str(kw))
        try:
            r = await self._func(**kw)
            return r
        except Exception as e:
            print (Exception, ":", e)


def add_route(app, fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not define in %s.', str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    app.router.add_route(method, path, RequestHandler(app, fn))

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
        positional_or_keyword_args = [name for name, param in func_items
                                      if param.kind == param.POSITIONAL_OR_KEYWORD]
        required_kw_args = [name for name, param in func_items
                            if param.kind == param.KEYWORD_ONLY
                            and param.default == inspect.Parameter.empty]
        need_args = [name for name, param in func_items
                         if param.kind == param.KEYWORD_ONLY
                         or param.kind == param.VAR_KEYWORD]
        any_args = [name for name, param in func_items
                         if param.kind == param.VAR_KEYWORD]
        for name, param in func_items:
            print(name, param.kind)
        print(request.match_info)
        if func_args:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest(text='Missing Content-Type.')
                ct = request.content_type.lower()
                if ct.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest(text="JSON body must be object.")
                    kw = params
                elif ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest(text='Unsupported Content-Type: %s' % request.content_type)
            if request.method == 'GET':
                qs = request.query_string
                if qs:
                    kw = dict()
                    for k, v in parse.parse_qs(qs, True).items():
                        kw[k] = v[0]
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if not any_args:
                copy = dict()
                for name in func_args:
                    if name in kw:
                        copy[name] = kw[name]
                kw = copy
            for k, v in request.match_info.items():
                if k in kw:
                    print("Duplicate arg name in named arg and kw args: %s" % k)
                kw[k] = v
        if 'request' == positional_or_keyword_args[-1]:
            kw['request'] = request
        if required_kw_args:
            for name in required_kw_args:
                if not name in kw:
                    return web.HTTPBadRequest(text="Missing argument: %s" % name)
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

def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)

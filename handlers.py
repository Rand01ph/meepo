import time
from aiohttp import web
import aiohttp_jinja2
from meepo.core import get, post
from models import User, Blog

@get('/')
async def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    context = {'blogs': blogs}
    response = aiohttp_jinja2.render_template('blogs.html',
                                              request,
                                              context)
    return response

@get('/users/')
async def users(request):
    users = await User.findAll()
    print(users)
    context = {
        'users': users
    }
    response = aiohttp_jinja2.render_template('test.html',
                                              request,
                                              context)
    return response

@get('/101/')
async def onezeroone(request):
    context = {}
    response = aiohttp_jinja2.render_template('101.html',
                                              request,
                                              context)
    return response

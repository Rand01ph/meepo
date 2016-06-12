from aiohttp import web
import aiohttp_jinja2
from meepo.core import get, post
from models import User


@get('/')
@aiohttp_jinja2.template('test.html')
async def index(request):
    users = await User.findAll()
    print(users)
    return {
        'users': users
    }

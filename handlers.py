from aiohttp import web
import aiohttp_jinja2
from meepo.core import get, post
from models import User


@get('/')
async def index(request):
    users = await User.findAll()
    print(users)
    context = {
        'users': users
    }
    response = aiohttp_jinja2.render_template('test.html',
                                              request,
                                              context)
    return response

import orm, asyncio, sys
from models import User

async def test():
    await orm.create_pool(loop=loop, user='www-data', password='WWW-data-123', db='meepo')
    u = User(name='Test3', email='test3@example.com', passwd='1234567890', image='about:blank')
    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()

if loop.is_closed():
    sys.exit(0)

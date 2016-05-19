#! /usr/bin/env python
# coding=utf-8
# author: Rand01ph

import asyncio, sys
from models import User
from meepo import orm

async def test():
    await orm.create_pool(loop=loop, user='www-data', password='WWW-data-123', db='meepo')
    u = User(name='Test3', email='test5@example.com', passwd='1234567890', image='about:blank')
    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()

if loop.is_closed():
    sys.exit(0)

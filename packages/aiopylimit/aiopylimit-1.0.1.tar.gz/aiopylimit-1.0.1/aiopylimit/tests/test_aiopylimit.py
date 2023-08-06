import asyncio
import redis.asyncio as aioredis
from unittest import IsolatedAsyncioTestCase

from aiopylimit import AIOPyRateLimit


class TestPyLimit(IsolatedAsyncioTestCase):

    async def test_throttle(self):
        AIOPyRateLimit.init(await aioredis.from_url("redis://localhost"))
        limit = AIOPyRateLimit(10, 10)
        for x in range(0, 20):
            await asyncio.sleep(.5)
            if x < 10:
                self.assertTrue(await limit.attempt('test_namespace'))
            else:
                self.assertFalse(await limit.attempt('test_namespace'))
        await asyncio.sleep(6)
        self.assertTrue(await limit.attempt('test_namespace'))

    async def test_peek(self):
        AIOPyRateLimit.init(await aioredis.from_url("redis://localhost"))
        limit = AIOPyRateLimit(10, 10)
        for x in range(0, 10):
            self.assertTrue(await limit.attempt('test_namespace2'))
        self.assertTrue(await limit.is_rate_limited('test_namespace2'))
        await asyncio.sleep(10)
        self.assertFalse(await limit.is_rate_limited('test_namespace2'))

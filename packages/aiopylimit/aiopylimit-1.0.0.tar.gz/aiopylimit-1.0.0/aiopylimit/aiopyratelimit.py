import time

from aiopylimit.aioredis_helper import AIORedisHelper
from aiopylimit.aiopyratelimit_exception import AIOPyRateLimitException


class AIOPyRateLimit(object):
    redis_helper = None  # type: AIORedisHelper

    def __init__(self, period, limit):
        self.period = period  # type: int
        self.limit = limit  # type: int

    @classmethod
    def init(cls, connection):
        """
        Initializes redis connection
        :param connection: the redis async connection object (from official library) 
        """
        cls.redis_helper = AIORedisHelper(connection)

    async def __can_attempt(self, namespace: str, add_attempt=True) -> bool:
        """
        Checks if a namespace is rate limited or not with
        including/excluding the current call

        :param namespace: Rate limiting namespace
        :type namespace: str

        :param add_attempt: Boolean value indicating if the current
        call should be considered as an attempt or not
        :type add_attempt: bool

        :return: Returns true if attempt can go ahead under current rate
        limiting rules, false otherwise
        """
        can_attempt = False
        if not AIOPyRateLimit.redis_helper:
            raise AIOPyRateLimitException(
                "redis connection information not provided")
        connection = await AIOPyRateLimit.redis_helper.get_atomic_connection()

        current_time = int(round(time.time() * 1000000))
        old_time_limit = current_time - (self.period * 1000000)
        connection.zremrangebyscore(namespace, 0, old_time_limit)

        connection.expire(namespace, self.period)
        if add_attempt:
            current_count = 0
            connection.zadd(namespace, {current_time: current_time})
        else:
            current_count = 1  # initialize at 1 to compensate
            # the case that this attempt is not getting counted
        connection.zcard(namespace)
        redis_result = await connection.execute()
        current_count += redis_result[-1]
        if current_count <= self.limit:
            can_attempt = True
        return can_attempt

    async def attempt(self, namespace: str):
        """
        Records an attempt and returns true of false depending on whether
        attempt can go through or not

        :param namespace: Rate limiting namespace
        :type namespace: str

        :return: Returns true if attempt can go ahead under current rate
        limiting rules, false otherwise
        """
        return await self.__can_attempt(namespace=namespace)

    async def is_rate_limited(self, namespace: str) -> bool:
        """
        Checks if a namespace is already rate limited or not without making
        any additional attempts

        :param namespace:  Rate limiting namespace
        :type namespace: str

        :return:    Returns true if attempt can go ahead under current rate
         limiting rules, false otherwise
        """
        return not await self.__can_attempt(namespace=namespace,
                                            add_attempt=False)

[![Build Status](https://travis-ci.org/dmarkey/aiopylimit.svg?branch=master)](https://travis-ci.org/dmarkey/aiopylimit)
# aiopylimit
A distributed rate limiting library for python using leaky bucket algorithm and Redis supporting asyncio

**version 1.0.0 is incompatible with previous version, sorry you need to give a redis connection from 1.0.0**
# Prerequisites
This library makes use of Redis and needs it as a prerequisite.
Make sure that Redis server is running before using this library

# Installation

```
pip install aiopylimit
```

# Example
This library uses the main `redis` library and takes a connection as an argument.

1.) Import the library
```
from aiopylimit import AIOPyRateLimit
```

2.) Initialize the library
```
import redis.asyncio as aioredis
AIOPyRateLimit.init(aioredis.from_url("redis://localhost"))
```

3.) Create a rate limit namespace
```
limit = AIOPyRateLimit(60, 100)     # rate limit period in seconds
                                    # no of attempts in the time period
```

4.) Record ant attempt and check if it is allowed or not
```
is_allowed = await limit.attempt('api_count')   # will return true if number of attempts
                                          # are less than or equal to 1000 in last 1 minute,
                                          # false otherwise
```

5.) In order to check if a namespace is already rate limited or not
```
is_rate_limited = await limit.is_rate_limited('api_count')  # will return true if this namespace is already rate limited, false otherwise
```

# Reference
https://engineering.classdojo.com/blog/2015/02/06/rolling-rate-limiter/

Based on https://github.com/biplap-sarkar/pylimit

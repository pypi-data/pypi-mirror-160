import multiprocessing
from urllib3 import connectionpool, poolmanager

# we're not able to make a configuration option for this at the moment.
# It's unlikely anyone would want to get past twice the numbers of CPU
# On the other hand, this potential waste is really minimal, compared to
# what we're otherwise doing (Selenium…)
MAX_CONN = multiprocessing.cpu_count() * 3


class HTTPConnectionPool(connectionpool.HTTPConnectionPool):
    def __init__(self, *args, **kwargs):
        # this block=True will avoid hard failures if the pool is full,
        # but there's still something that flips it back to False sometimes
        # in those tests.
        kwargs.update(maxsize=MAX_CONN, block=True)
        super(HTTPConnectionPool, self).__init__(*args, **kwargs)


class HTTPSConnectionPool(connectionpool.HTTPSConnectionPool):
    def __init__(self, *args, **kwargs):
        # this block=True will avoid hard failures if the pool is full,
        # but there's still something that flips it back to False sometimes
        # in those tests.
        kwargs.update(maxsize=MAX_CONN, block=True)
        super(HTTPSConnectionPool, self).__init__(*args, **kwargs)


registry = poolmanager.pool_classes_by_scheme
registry['http'] = HTTPConnectionPool
registry['https'] = HTTPSConnectionPool

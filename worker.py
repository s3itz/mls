import os
import redis
from rq import Worker, Queue, Connection

redis_url = os.getenv('MLS_REDIS_URI', 'redis://localhost:6379')

listen = ['high', 'normal', 'low']

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listne)))
        worker.work()
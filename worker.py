import urllib.parse
from redis import Redis
from rq import Worker, Queue, Connection
from mls import app

listen = ['high', 'default', 'low']

redis_url = app.config.get('REDIS_URI')
if not redis_url:
    raise RuntimeError('Set up Redis To Go first.')

urllib.parse.uses_netloc.append('redis')
url = urllib.parse.urlparse(redis_url)
print(url)
conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
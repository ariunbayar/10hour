import time
import redis


def cacheSet(key, value):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(key, value)

def cacheGet(name):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    return r.get(name)

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    contentBegin = """
    <!DOCTYPE HTML>
    <html>
    <head>
        <link href='/static/favicon.png' rel='shortcut icon' />
    </head>
    <body>
    """

    cacheSet('hello', 'hello world!')
    contentBody = cacheGet('hello')

    contentEnd = """
    </body>
    </html>
    """
    content = contentBegin + contentBody + contentEnd
    return [content]

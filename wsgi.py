import re
import os
import sqlite3
import redis
import time
import hashlib


def full_path_to(relative_file_path):
    # translates relative file path to absolute
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(cur_dir, relative_file_path)


def render_homepage(session_id):
    content = open(full_path_to('templates/main.html'), 'r').read()
    return content, 'text/html'


def render_start(session_id):
    begin_time = str(time.time())
    cache_set(session_id, begin_time)
    return 'OK', 'text/plain'


def render_finish(session_id):
    begin_time = cache_get(session_id)
    if begin_time:
        official_finish_seconds = 36000
        if time.time() - float(begin_time) > official_finish_seconds:
            return '1', 'text/plain'

    return '0', 'text/plain'


def render_404(session_id):
    return 'page not found', 'text/plain'


routes = {
    '/': render_homepage,
    '/start': render_start,
    '/finish': render_finish,
}


# http://www.tutorialspoint.com/sqlite/sqlite_python.htm
# https://docs.python.org/2/library/sqlite3.html
def db_connect():
    conn = sqlite3.connect(full_path_to('10hour.db'))
    return conn


def db_migrate(cursor):
    """ Import database schema """
    cursor.execute('DROP TABLE user;')
    cursor.execute('''
        CREATE TABLE user (
            id      INTEGER PRIMARY KEY,
            name    TEXT
        )
    ''')


def db_demo():
    conn = db_connect()
    with conn:
        cursor = conn.cursor()
        # db_migrate(cursor)
        cursor.execute("INSERT INTO user (name) VALUES ('Paul')")
        # last_id = cursor.lastrowid  # Get last insert id
        # data = cursor.fetchone()
        cursor.execute("SELECT * FROM user")
        for id, name in cursor.fetchall():
            print "id: %s, name: %s" % (id, name)


def cache_set(key, value):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set(key, value)


def cache_get(name):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    return r.get(name)


def application(env, start_response):
    headers = []
    session_id = ''

    is_cookie_set = False
    if 'HTTP_COOKIE' in env:
        matches = re.search('session_id=([0-9a-f]{32})', env['HTTP_COOKIE'])
        if matches:
            is_cookie_set = True
            session_id = matches.group(1)

    if not is_cookie_set:
        data = str(time.time()) + env.get('REMOTE_ADDR')
        session_id = hashlib.md5(data).hexdigest()
        headers.append(('Set-Cookie', 'session_id=%s;' % session_id))

    uri = env.get('REQUEST_URI')
    if uri in routes:
        content, content_type = routes[uri](session_id)
    else:
        content, content_type = render_404(session_id)

    headers.append(('Content-Type', content_type))
    start_response('200 OK', headers)

    return [content]

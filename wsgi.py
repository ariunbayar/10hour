import os
import sqlite3
import redis


# http://www.tutorialspoint.com/sqlite/sqlite_python.htm
# https://docs.python.org/2/library/sqlite3.html
def db_connect():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(cur_dir + '/10hour.db')
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
    start_response('200 OK', [('Content-Type', 'text/html')])

    cache_set('hello', 'hello world!')

    content = """
        <!DOCTYPE HTML>
        <html>
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />

            <title>JWPlayer for 10hour</title>
            <link href='/static/favicon.png' rel='shortcut icon' />
            <script src="/static/jwplayer.js"></script>
            <script>jwplayer.key="BSxpAaTPudTB38Uc3YCYtneTFkEHaq90o/XEUw==";</script>
        </head>
        <body>

        %s
        <div id="myElement">Loading the player...</div>
        <script type="text/javascript">
            jwplayer("myElement").setup({
                file:  "/media/whatislove.flv",
                image: "/media/what_is_love_cover.png",
                autostart: true,
                //mute: true,
                repeat: true,
                width: 640,
                height: 360
            });
        </script>


        </body>
        </html>
    """ % cache_get('hello')

    return [content]

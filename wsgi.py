import re
import os
import sqlite3
import redis
import time
import hashlib


def render_homepage(session_id):
    cache_set('hello', 'hello world!')
    content = """
        <!DOCTYPE HTML>
        <html>
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />

            <title>JWPlayer for 10hour</title>
            <link href='/static/favicon.png' rel='shortcut icon' />
            <script src="/static/jwplayer.js"></script>
            <script src="/static/jquery-2.0.3.min.js"></script>
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

	    function im_start() {
		$.get('/start', {}, function (data){
			if (data == 'OK') {
			   setTimeout(first_blood, 5000);
			} else {
			   setTimeout(im_start, 500);
			}
		});
            }
	    function im_finish() {
		$.get('/finish', {}, function (data){
			if (data == '1') {
			   console.log('finish');
			} else {
			   setTimeout(im_finish, 500);
			}
		});
	    }
	    function first_blood() {
		alert('FIRST BLOOD!');
		setTimeout(double_kill, 5000);
	    }
	    function double_kill() {
		alert('DOUBLE KILL!');
		setTimeout(triple_kill, 5000);
	    }
	    function triple_kill() {
		alert('TRIPLE KILL!');
		im_finish();
	    }
	    im_start();
        </script>


        </body>
        </html>
    """ % cache_get('hello')
    return content, 'text/html'


def render_start(session_id):
    return 'OK', 'text/plain'


def render_finish(session_id):
    # returns 1 or 0
    return '1', 'text/plain'


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

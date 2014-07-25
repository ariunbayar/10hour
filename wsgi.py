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
		$.post({
		    '10hour.uwen.mn', function (data) {
			if (data == 'Ok') {
			   alert('Time started')
			   setTimeout(function(){ firls_blood()}, 5000);
			} else {
			   setTimeout(function(){ im_start()}, 500);
			}
		    }
		});
            }
	    function first_blood() {
		alert('FIRST BLOOD!');
		setTimeout(function(){ double_kill()}, 10000);
	    }
	    function double_kill() {
		alert('DOUBLE KILL!');
		setTimeout(function(){ triple_kill()}, 10000);
	    }
	    function triple_kill() {
		alert('TRIPLE KILL!');
		im_finish();
	    }
	    function im_finish() {
		$.ajax(
		url:''

		);
	    }
	    im_start();

        </script>


        </body>
        </html>
    """ % cache_get('hello')

    return [content]

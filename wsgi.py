import re
import os
import sqlite3
import redis
import time
import hashlib


def render_homepage(session_id):
    content = """
        <!DOCTYPE HTML>
        <html>
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />

            <title>JWPlayer for 10hour</title>
            <link href='/static/favicon.png' rel='shortcut icon' />
            <link rel="stylesheet" type="text/css" href="/static/css/main.css"/>
            <script src="/static/jwplayer.js"></script>
            <script src="/static/jquery-2.0.3.min.js"></script>
            <script>jwplayer.key="BSxpAaTPudTB38Uc3YCYtneTFkEHaq90o/XEUw==";</script>
        </head>
        <body>

        <div class="header">
            <h1>10hour</h1>
        </div>
        <div class="content">
        <div class="video">
            <div id="main_video" class="video">Loading the player...</div>
        </div>
        <script type="text/javascript">
            jwplayer("main_video").setup({
                file:  "/media/what_is_love.flv",
                image: "/media/what_is_love_cover.jpg",
                autostart: true,
                //mute: true,
                repeat: true,
                width: 640,
                height: 360
            });

            var colors = [
            'AliceBlue',
            'AntiqueWhite',
            'Aqua',
            'Aquamarine',
            'Azure',
            'Beige',
            'Bisque',
            'Black',
            'BlanchedAlmond',
            'Blue',
            'BlueViolet',
            'Brown',
            'BurlyWood',
            'CadetBlue',
            'Chartreuse',
            'Chocolate',
            'Coral',
            'CornflowerBlue',
            'Cornsilk',
            'Crimson',
            'Cyan',
            'DarkBlue',
            'DarkCyan',
            'DarkGoldenRod',
            'DarkGray',
            'DarkGreen',
            'DarkKhaki',
            'DarkMagenta',
            'DarkOliveGreen',
            'DarkOrange',
            'DarkOrchid',
            'DarkRed',
            'DarkSalmon',
            'DarkSeaGreen',
            'DarkSlateBlue',
            'DarkSlateGray',
            'DarkTurquoise',
            'DarkViolet',
            'DeepPink',
            'DeepSkyBlue',
            'DimGray',
            'DodgerBlue',
            'FireBrick',
            'FloralWhite',
            'ForestGreen',
            'Fuchsia',
            'Gainsboro',
            'GhostWhite',
            'Gold',
            'GoldenRod',
            'Gray',
            'Green',
            'GreenYellow',
            'HoneyDew',
            'HotPink',
            'IndianRed',
            'Indigo',
            'Ivory',
            'Khaki',
            'Lavender',
            'LavenderBlush',
            'LawnGreen',
            'LemonChiffon',
            'LightBlue',
            'LightCoral',
            'LightCyan',
            'LightGoldenRodYellow',
            'LightGray',
            'LightGreen',
            'LightPink',
            'LightSalmon',
            'LightSeaGreen',
            'LightSkyBlue',
            'LightSlateGray',
            'LightSteelBlue',
            'LightYellow',
            'Lime',
            'LimeGreen',
            'Linen',
            'Magenta',
            'Maroon',
            'MediumAquaMarine',
            'MediumBlue',
            'MediumOrchid',
            'MediumPurple',
            'MediumSeaGreen',
            'MediumSlateBlue',
            'MediumSpringGreen',
            'MediumTurquoise',
            'MediumVioletRed',
            'MidnightBlue',
            'MintCream',
            'MistyRose',
            'Moccasin',
            'NavajoWhite',
            'Navy',
            'OldLace',
            'Olive',
            'OliveDrab',
            'Orange',
            'OrangeRed',
            'Orchid',
            'PaleGoldenRod',
            'PaleGreen',
            'PaleTurquoise',
            'PaleVioletRed',
            'PapayaWhip',
            'PeachPuff',
            'Peru',
            'Pink',
            'Plum',
            'PowderBlue',
            'Purple',
            'Red',
            'RosyBrown',
            'RoyalBlue',
            'SaddleBrown',
            'Salmon',
            'SandyBrown',
            'SeaGreen',
            'SeaShell',
            'Sienna',
            'Silver',
            'SkyBlue',
            'SlateBlue',
            'SlateGray',
            'Snow',
            'SpringGreen',
            'SteelBlue',
            'Tan',
            'Teal',
            'Thistle',
            'Tomato',
            'Turquoise',
            'Violet',
            'Wheat',
            'White',
            'WhiteSmoke',
            'Yellow',
            'YellowGreen',
            ];

            window.color_idx = 0;

            function notify(message, time) {
                var li = $('<li>');
                $('.notification').prepend(li);
                var el_msg = $('<div>');
                var el_time = $('<div>');
                li.append(el_msg).append(el_time);
                el_msg.html(message);
                el_time.html(time);
                window.color_idx = ~~(Math.random() * colors.length)
                el_msg.css('color', colors[window.color_idx]);
                //window.color_idx++;
            }

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
                       notify('Finished', '');
                    } else {
                       setTimeout(im_finish, 1000);
                    }
                });
            }

            function first_blood() {
                notify('FIRST BLOOD!', '5 sec');
                setTimeout(double_kill, 5000);
            }

            function double_kill() {
                notify('DOUBLE KILL!', '10 sec');
                setTimeout(triple_kill, 5000);
            }

            function triple_kill() {
                notify('TRIPLE KILL!', '15 sec');
                im_finish();
            }
            im_start();
        </script>

        <ul class="notification">
            <li><div>Started</div><div></div></li>
        </ul>
        </div>
        <div class="footer">&copy; 2014</div>

        </body>
        </html>
    """
    return content, 'text/html'


def render_start(session_id):
    begin_time = str(time.time())
    cache_set(session_id, begin_time)
    return 'OK', 'text/plain'


def render_finish(session_id):
    begin_time = cache_get(session_id)
    if begin_time:
        official_finish_seconds = 30
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

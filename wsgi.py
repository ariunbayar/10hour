import os
import sqlite3


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

def db_demo(conn):
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


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    content = """
    <!DOCTYPE HTML>
    <html>
    <head>
        <link href='/static/favicon.png' rel='shortcut icon' />
    </head>
    <body>
        Hello World!
    </body>
    </html>
    """
    return [content]


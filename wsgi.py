import time


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

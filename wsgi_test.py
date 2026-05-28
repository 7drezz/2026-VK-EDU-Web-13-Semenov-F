import urllib.parse

def application(environ, start_response):
    get_params = {}
    qs = environ.get('QUERY_STRING', '')
    if qs:
        for pair in qs.split('&'):
            if '=' in pair:
                key, val = pair.split('=', 1)
                get_params[key] = val
    
    post_params = {}
    if environ.get('REQUEST_METHOD') == 'POST':
        try:
            length = int(environ.get('CONTENT_LENGTH', 0))
            if length > 0:
                body = environ['wsgi.input'].read(length).decode('utf-8')
                for pair in body.split('&'):
                    if '=' in pair:
                        key, val = pair.split('=', 1)
                        post_params[key] = val
        except:
            pass
    
    html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>WSGI Test</title></head><body>'
    html += '<h1>WSGI Test</h1>'
    html += '<h2>GET params:</h2><ul>'
    
    if get_params:
        for k, v in get_params.items():
            html += f'<li>{k} = {v}</li>'
    else:
        html += '<li>none</li>'
    
    html += '</ul><h2>POST params:</h2><ul>'
    
    if post_params:
        for k, v in post_params.items():
            html += f'<li>{k} = {v}</li>'
    else:
        html += '<li>none</li>'
    
    html += '</ul>'
    html += '<form method="post"><input name="test" placeholder="test"><button type="submit">Send</button></form>'
    html += '<p><a href="?a=1&b=2">Test GET</a></p>'
    html += '</body></html>'
    
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [html.encode()]

from http.server import BaseHTTPRequestHandler
import json
import os

arquivo_mock = os.path.join(os.path.dirname(__file__), 'mock.json')

def read_mock(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as arq:
        return json.load(arq)

class SimpleRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, response_code=200, content_type='application/json'):
        self.send_response(response_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_response()
            dados = read_mock(arquivo_mock)
            self.wfile.write(json.dumps(dados).encode('utf-8'))
        else:
            self._set_response(404)
            response = {'error': 'Not Found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        if self.path == '/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Process the data here
            response = {'received': data}
            self._set_response()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_response(404)
            response = {'error': 'Not Found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def handler(event, context):
    class FakeServer:
        def __init__(self, method, path, body):
            self.method = method
            self.path = path
            self.body = body

        def makefile(self, *args, **kwargs):
            return self

        def readline(self):
            return self.body

    class FakeRequestHandler(SimpleRequestHandler):
        def __init__(self, request, client_address, server):
            self.rfile = FakeServer(event['httpMethod'], event['path'], event.get('body', ''))
            self.wfile = server
            self.client_address = client_address
            self.server = server
            self.headers = event.get('headers', {})

    server = FakeServer(event['httpMethod'], event['path'], event.get('body', ''))
    handler_instance = FakeRequestHandler(server, None, None)

    if event['httpMethod'] == 'GET':
        handler_instance.do_GET()
    elif event['httpMethod'] == 'POST':
        handler_instance.do_POST()

    return server.wfile

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
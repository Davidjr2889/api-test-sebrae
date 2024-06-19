from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os

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

def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=int(os.getenv('PORT', 8000))):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

# Caminho para o arquivo mock.json
arquivo_mock = os.path.join(os.path.dirname(__file__), 'mock.json')

# Função para ler o conteúdo do mock.json
def read_mock(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as arq:
        return json.load(arq)

# Definindo a classe do request handler
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
            
            # Processando os dados recebidos
            response = {'received': data}
            self._set_response()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_response(404)
            response = {'error': 'Not Found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

# Função handler para o Vercel
def handler(event, context):
    if event['httpMethod'] == 'GET':
        if event['path'] == '/':
            response = {
                'statusCode': 200,
                'body': json.dumps(read_mock(arquivo_mock)),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            response = {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not Found'}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    elif event['httpMethod'] == 'POST':
        if event['path'] == '/data':
            data = json.loads(event['body'])
            response = {
                'statusCode': 200,
                'body': json.dumps({'received': data}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            response = {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not Found'}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    else:
        response = {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method Not Allowed'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    return response

# Executando o servidor localmente
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
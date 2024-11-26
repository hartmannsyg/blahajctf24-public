import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/decrypt'):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            if 'addr' in query_params:
                file_name = f"{query_params['addr'][0]}.exe"
                if os.path.exists(file_name):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
                    self.end_headers()
                    with open(file_name, 'rb') as file:
                        self.wfile.write(file.read())
                else:
                    self.send_error(404, f"File not found: {file_name}")
            else:
                self.send_error(400, "Bad request: 'addr' parameter missing in query string")
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        if self.path == '/new':
            self.send_response(200)
            # self.wfile.close()
        elif self.path == '/new':
            self.send_response(200)
            # self.wfile.close()
        else:
            self.send_error(404, "Not Found")


PORT = 8000

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()

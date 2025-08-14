from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot rodando!')

def start_server():
    port = int(os.getenv("PORT", 10000))  # Render define a porta em PORT
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

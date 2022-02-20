import http.server
from socketserver import ThreadingMixIn
import threading
import json, re

class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    def shutdown(self):
        self.socket.close()
        http.server.HTTPServer.shutdown(self)

def route(path):
    def _route(f):
        setattr(f, '__route__', path)
        return f
    return _route

def read_params(path):
    query = path.split('?')
    if len(query) > 1:
        query = query[1].split('&')
        return dict(map(lambda x: x.split('='), query))

def get(req_handler, routes):
    for name, handler in routes.__class__.__dict__.items():
        if hasattr(handler, "__route__"):
            if None != re.search(handler.__route__, req_handler.path):
                req_handler.send_response(200)
                req_handler.send_header('Content-Type', 'application/json')
                req_handler.send_header('Access-Control-Allow-Origin', '*')
                req_handler.end_headers()
                params = read_params(req_handler.path)
                data = json.dumps(handler(routes, params)) + '\n'
                req_handler.wfile.write(bytes(data,  encoding = 'utf-8'))
                return

def run(routes, host = '0.0.0.0', port = 8080):
    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args, **kwargs):
            pass
        def do_GET(self):
            get(self, routes)
    server = ThreadedHTTPServer((host, port), RequestHandler)
    thread = threading.Thread(target = server.serve_forever)
    thread.daemon = True
    thread.start()
    print (f"HTTP server started on port {port}")

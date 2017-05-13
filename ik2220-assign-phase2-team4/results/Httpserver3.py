from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import SocketServer

class ThreadingServer(ThreadingMixIn,HTTPServer):
    pass
class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>ws3,Hello!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        length = int(self.headers['Content-Length']) 
        data = self.rfile.read(length) 
        self._set_headers()
        self.wfile.write("<html><body><h1>ws3,POST!</h1><pre>" + data + "</pre></body></html>")
        
def run(server_class=ThreadingServer, handler_class=Handler, port=80):
    server_address = ('100.0.0.42', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting http...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

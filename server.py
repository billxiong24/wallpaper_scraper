"""HTTP server to serve req"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from scrape import scrape
import urlparse

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_qs = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        print(parsed_qs)
        start = parsed_qs.get('start', None)
        end = parsed_qs.get('end', None)


        


        return 0        



def run(ip, port):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()


run('localhost', 8081)

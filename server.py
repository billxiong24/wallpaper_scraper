"""HTTP server to serve req"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from scrape import scrape
import urlparse
import json

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_qs = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        start = parsed_qs.get('start', None)
        end = parsed_qs.get('end', None)

        file_list = scrape(start, end)

        res = json.dumps(file_list)

        # with open("test.jpg", "wb") as handle:
            # handle.write(file_list[0]['data'])
        self.send_header("Content-type", "json")
        self.end_headers()

        self.wfile.write(res)

        return 0        



server_address = ('127.0.0.1', 8081)
httpd = HTTPServer(server_address, RequestHandler)
httpd.serve_forever()

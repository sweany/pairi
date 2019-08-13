#! /usr/bin/env python3

# Custom PurpleAir data handler
# You need to have your own DNS service set the host(A) record for api.thingspeak.com
#
# https://blog.anvileight.com/posts/simple-python-http-server/
# https://it.megocollector.com/linux/add-custom-dns-entries-to-pi-hole/

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import ssl
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #print(self.command, self.path)
        bits = urlparse(self.path)
        #print(bits.query)
        print(json.dumps(parse_qs(bits.query)))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


#httpd = HTTPServer(('0.0.0.0', 443), BaseHTTPRequestHandler)
httpd = HTTPServer(('0.0.0.0', 443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile="/etc/ssl/private/ssl-cert-snakeoil.key",
        certfile='/etc/ssl/certs/ssl-cert-snakeoil.pem', server_side=True)

httpd.serve_forever()


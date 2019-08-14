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
import requests
from datetime import datetime
from collections import OrderedDict

logfile = '/var/log/pairi.log'
fh = open(logfile, 'a')

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%z")
        print(self.command, self.path, self.headers)
        bits = urlparse(self.path)
        #print(bits.query)
        data = parse_qs(bits.query)
        print(json.dumps(data))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

        # write data to log file
        print()
        data['datetime'] = ts
        o = OrderedDict(data)
        o.move_to_end('key', last=False)
        o.move_to_end('datetime', last=False)
        fh.write(json.dumps(o) + "\n")
        fh.flush()
        

        # forward the request on to the real destination
        headers = { 'Host': 'api.thingspeak.com', 'User-Agent': 'PurpleAir/4.02' }
        url = 'https://34.226.171.107' + self.path
        print('forwarding request to ' + url)
        try:
            r = requests.get(url, headers=headers, verify=False)
        except BaseException as e:
            print("Exception: {}".format(e))
        
        print(r.status_code)
        print(r.text)

        print()

#httpd = HTTPServer(('0.0.0.0', 443), BaseHTTPRequestHandler)
httpd = HTTPServer(('0.0.0.0', 443), SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile="/etc/ssl/private/ssl-cert-snakeoil.key",
        certfile='/etc/ssl/certs/ssl-cert-snakeoil.pem', server_side=True)

httpd.serve_forever()


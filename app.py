
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps
import sys
from urllib.parse import urlparse
from urllib.parse import parse_qs
""" The HTTP request handler """
class RequestHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def send_dict_response(self, d):
        """ Sends a dictionary (JSON) back to the client """
        self.wfile.write(bytes(dumps(d), "utf8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
        data = sys.stdin.read()

        response = {}
        response["status"] = "OK"
        self.send_dict_response(response)

    def do_POST(self):
        enc = sys.getfilesystemencoding()
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        dataLength = int(self.headers["Content-Length"])
        rowPostData = self.rfile.read(dataLength)
        postData = rowPostData.decode()
        
        print(rowPostData)
        print(postData)
        print(len(postData))
        response = {}
        response["status"] = "OK_post"
        self.send_dict_response(response)


print("Starting server")
httpd = HTTPServer(("127.0.0.1", 8000), RequestHandler)
print("Hosting server on port 8000")
httpd.serve_forever()

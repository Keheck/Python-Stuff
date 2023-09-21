import http.server
from os.path import isfile, join
from os import getcwd

class RequestHandler(http.server.BaseHTTPRequestHandler): 
    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header("Location", "/page.html")
            self.end_headers()
        if not isfile(join(getcwd(), "http", self.path[1:])):
            self.send_response(404)
            self.end_headers()
        with open(join(getcwd(), "http", self.path[1:])) as fh:
            text = "\n".join(fh.readlines())
            self.send_response(200, text)
            self.end_headers()


with http.server.HTTPServer(("127.0.0.1", 80), RequestHandler) as httpd:
    print("Serving at 80")
    httpd.serve_forever()

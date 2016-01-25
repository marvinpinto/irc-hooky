import BaseHTTPServer
import sys
import time
import json
from irc_hooky.entrypoint import handler


HOST_NAME = sys.argv[1]
PORT_NUMBER = int(sys.argv[2])


def handle_github_hook(payload, headers):
    event = {
        "X-Hub-Signature": headers.get("X-Hub-Signature"),
        "X-Github-Event": headers.get("X-Github-Event"),
        "resource-path": "/github",
        "irc-server": "chat.freenode.net",
        "irc-port": 6667,
        "irc-channel": "##testtest",
        "payload": payload
    }
    return handler(event, {})


class LocalIRCHooky(BaseHTTPServer.BaseHTTPRequestHandler):

    server_version = "LocalIRCHooky/0.1"

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Nothing to see here!")

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        payload = json.loads(post_data)
        if (self.path == "/github"):
            result = handle_github_hook(payload, self.headers)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(result)


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), LocalIRCHooky)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

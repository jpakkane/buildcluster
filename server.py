#!/usr/bin/env python3

q#  Copyright (C) 201 Jussi Pakkanen.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of version 3, or (at your option) any later version,
# of the GNU General Public License as published
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import socket
import threading
import socketserver
import pickle

import concurrent.futures


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        import time
        try:
            o = pickle.loads(self.request.recv(1024))
        except Exception as e:
            print(e)
        print('Query:', o)
        time.sleep(2)
        reply = 'foo'
        self.request.sendall(pickle.dumps(reply))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 6667

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    print(ip, port)
    server.serve_forever()
    server.server_close()

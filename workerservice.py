#!/usr/bin/env python3

#  Copyright (C) 201 Jussi Pakkanen.
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
import sys

import concurrent.futures

import bprotocol
import subprocess

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        import time
        try:
            o = pickle.loads(self.request.recv(1024))
        except Exception as e:
            print(e)
        assert isinstance(o, bprotocol.BuildRequest)
        assert(o.id == bprotocol.BUILD_REQUEST_ID)
        pc = subprocess.call(o.command, cwd=o.path)
        reply = bprotocol.BuildResult(pc.returncode, pc.stdout, pc.stderr)
        self.request.sendall(pickle.dumps(reply))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('127.0.0.1', 1))
        return s.getsockname()[0]
    finally:
        s.close()

def register_self(master_host):
    current_host = get_current_ip()
    msg = bprotocol.RegisterWorker(current_host)
    bprotocol.client(msg, master_host, bprotocol.MASTER_PORT)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('%s master_host' % sys.argv[0])
    print('THIS SERVICE IS EXTREMELY UNSECURE!')
    print('ONLY USE FOR TESTING IN CLOSED NETWORKS!')
    HOST = 'localhost'
    master_host = sys.argv[1]
    register_self(master_host)

    server = ThreadedTCPServer((HOST, bprotocol.WORKER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    print(ip, port)
    server.serve_forever()
    server.server_close()

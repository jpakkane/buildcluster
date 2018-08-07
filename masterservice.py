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

import concurrent.futures

import bprotocol

class WorkerList:
    
    def __init__(self):
        self.worker_list = []
        self.lock = threading.Lock()
        self.current_worker = 0

    def add_worker(self, worker):
        with self.lock:
            self.worker_list.append(worker)

    def get_worker(self):
        with self.lock:
            if len(self.worker_list) == 0:
                return None
            self.current_worker += 1
            if self.current_worker >= len(self.worker_list):
                self.current_worker = 0
            return self.worker_list[self.current_worker]


wlist = WorkerList()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        import time
        try:
            query = pickle.loads(self.request.recv(1024))
        except Exception as e:
            print(e)
        assert hasattr(query, 'id')
        if query.id == bprotocol.BUILD_REQUEST_ID:
            worker = wlist.get_worker()
            if worker is None:
                reply = bprotocol.BuildResult(1, b'No workers available', b'')
            else:
                reply = client.client(query, worker, bprotocol.WORKER_PORT)
            self.request.sendall(pickle.dumps(reply))
        elif query.id == bprotocol.WORKER_REGISTER_ID:
            print('Added new host:', query.host)
            wlist.add_worker(query.host)
            self.request.sendall(pickle.dumps(bprotocol.Ack()))
        else:
            pass

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST = "localhost"
    print('THIS SERVICE IS EXTREMELY UNSECURE!')
    print('ONLY USE FOR TESTING IN CLOSED NETWORKS!')

    server = ThreadedTCPServer((HOST, bprotocol.MASTER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    print(ip, port)
    server.serve_forever()
    server.server_close()


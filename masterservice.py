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
        self.worker_list = {}
        self.lock = threading.Lock()
        self.current_worker = 0

    def add_worker(self, worker):
        with self.lock:
            self.worker_list[worker] = 0

    def get_worker(self):
        with self.lock:
            if len(self.worker_list) == 0:
                return None
            smallest_load = 9999999
            lowest_worker = None
            for key, value in self.worker_list.items():
                if value < smallest_load:
                    smallest_load = value
                    lowest_worker = key
            assert(lowest_worker is not None)
            self.worker_list[lowest_worker] += 1
            return lowest_worker

    def release_worker(self, worker):
        with self.lock:
            self.worker_list[worker] -= 1

wlist = WorkerList()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        query = bprotocol.read_pickle_object(self.request)
        assert(hasattr(query, 'id'))
        if query.id == bprotocol.BUILD_REQUEST_ID:
            worker = wlist.get_worker()
            if worker is None:
                reply = bprotocol.BuildResult(1, b'No workers available', b'')
            else:
                try:
                    reply = bprotocol.client(query, worker, bprotocol.WORKER_PORT)
                finally:
                    wlist.release_worker(worker)
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
    HOST = ""
    print('THIS SERVICE IS EXTREMELY INSECURE!')
    print('ONLY USE FOR TESTING IN CLOSED NETWORKS!')

    server = ThreadedTCPServer((HOST, bprotocol.MASTER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    print(ip, port)
    server.serve_forever()
    server.server_close()


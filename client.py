#!/usr/bin/env python3

#  Copyright (C) 2018 Jussi Pakkanen.
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
import pickle
import sys

import bprotocol


def client(query, ip, port):
    assert(isinstance(query, (bprotocol.BuildRequest, bprotocol.RegisterSlave)))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1)
    sock.connect((ip, port))
    try:
        sock.sendall(pickle.dumps(query))
        d = sock.recv(1024)
        reply = pickle.loads(d)
        assert(reply.id == bprotocol.BUILD_RESULT_ID or reply.id == bprotocol.ACK_ID)
        return reply
    finally:
        sock.close()

if __name__ == "__main__":
    HOST = "localhost"

    query = bprotocol.BuildRequest('/tmp', ['sh', '-c', 'sleep 1; echo hello'])
    reply = client(query, HOST, bprotocol.MASTER_PORT)
    print(reply.stdout.decode(encoding='utf-8', errors='ignore'))
    print(reply.stderr.decode(encoding='utf-8', errors='ignore'), file=sys.stderr)
    sys.exit(reply.returncode)

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
import sys, os
import subprocess

import bprotocol

if __name__ == "__main__":
    HOST = "localhost" # sys.argv[1]
    cmd = sys.argv[2:]

    if 'FORCE_LOCAL' in os.environ:
        sys.exit(subprocess.run(cmd).returncode)
    query = bprotocol.BuildRequest(os.getcwd(), cmd)
    reply = bprotocol.client(query, HOST, bprotocol.MASTER_PORT)
    print(reply.stdout.decode(encoding='utf-8', errors='ignore'))
    print(reply.stderr.decode(encoding='utf-8', errors='ignore'), file=sys.stderr)
    sys.exit(reply.returncode)

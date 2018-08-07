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

import os

MASTER_PORT = 7776
SLAVE_PORT = 6667

BUILD_REQUEST_ID = 0
BUILD_RESULT_ID = 1
SLAVE_REGISTER_ID = 2

class BuildRequest:
    def __init__(self, path, command):
        assert(os.path.isabs(path))
        assert(isinstance(command, list))
        self.id = BUILD_REQUEST_ID
        self.path = path
        self.command = command

class BuildResult:
    def __init__(self, returncode, stdout, stderr):
        assert(isinstance(returncode, int))
        assert(isinstance(stdout, bytes))
        assert(isinstance(stderr, bytes))
        self.id = BUILD_RESULT_ID
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

class RegisterSlave:
    def __init__(self, address, num_cpus):
        self.id = SLAVE_REGISTER_ID
        self.address = address
        self.num_cpus = num_cpus

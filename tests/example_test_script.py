# Copyright (c) 2016, Nordic Semiconductor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of Nordic Semiconductor ASA nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Example demonstrating programming tool (in this case nrfjprog.exe) verification running tests provided in nrf52-production-programming/tests/.

"""

import subprocess
import sys
import unittest

from pynrfjprog import API


class TestProgrammingTool(unittest.TestCase):
    """
    This class will run each unit test for the specific programming tool.

    """

    @classmethod
    def setUpClass(cls):
        cls.api = setup_api()

    @classmethod
    def tearDownClass(cls):
        cleanup_api(cls.api)

    def setUp(self):
        self.api.recover()

    def tearDown(self):
        pass

    def test_uicr_write(self):
        run_exe(['-f', 'NRF52', '--program', 'test_uicr_write/hex/test_uicr_write.hex'])
        self.api.sys_reset()

        assert(self.api.read_u32(0x10001080) == 0xDEADBEEF)

    def test_ctrlap_protection_enabled(self):
        run_exe(['-f', 'NRF52', '--program', 'test_ctrlap_protection_enabled/hex/test_ctrlap_protection_enabled.hex'])
        self.api.sys_reset()

        self.api.recover()
        assert(self.api.read_u32(0x0) == 0xFFFFFFFF)


def run_exe(cmd):
    """
    Run nrfjprog with the given commands.

    :param list cmd: Commands to run nrfjprog with.
    """
    command = []
    command.append('nrfjprog')
    command.extend(cmd)
    return subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def setup_api():
    """
    Initialize api and connect to the target device.

    :return Object api: Instance of API that is initialized and connected to the target device, ready to be used.
    """
    api = API.API('NRF52') # TODO: Should not be hard coded.
    api.open()
    api.connect_to_emu_without_snr() # TODO: Should have the option for snr.
    return api

def cleanup_api(api):
    api.disconnect_from_emu()
    api.close()
    api = None


if __name__ == '__main__':
    """
    Run the tests with specified options.

    """
    unittest.main(verbosity = 2) # TODO: Run tests in a way where specific Test Cases can be run or the entire suite.

#
# Copyright (C) 2012-2020 Euclid Science Ground Segment
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 3.0 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#

import os
import unittest

from ElementsKernel.Temporary import TempDir, TempEnv

from ElementsServices.DataSync import \
    ConnectionConfiguration, DependencyConfiguration, \
    IrodsSynchronizer, WebdavSynchronizer, createSynchronizer


from fixtures.ConfigFilesFixture import theDependencyConfig, theWebdavFrConfig, theIrodsFrConfig

class TestDataSynchronizerMaker(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.m_top_dir = TempDir(prefix="DataSync_test")
        self.m_env = TempEnv()
        self.m_env["WORKSPACE"] = os.path.join(self.m_top_dir.path(), "workspace")
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        del self.m_top_dir

    def checkSynchronizerCreation(self, connection_config, expected_synchronizer):
        connection = ConnectionConfiguration(connection_config)
        dependency = DependencyConfiguration(theDependencyConfig(), connection.local_root)
        synchronizer = createSynchronizer(connection, dependency)
        assert type(synchronizer), expected_synchronizer

    def testSynchronizerCreation(self):
        webdav_configs = {
            theWebdavFrConfig(): WebdavSynchronizer,
        }
        irods_configs = {
            theIrodsFrConfig(): IrodsSynchronizer
        }
        if not IrodsSynchronizer.irodsIsInstalled():
            irods_configs = {}
        configs = webdav_configs.copy()
        configs.update(irods_configs)
        for config, expected in configs.items():
            self.checkSynchronizerCreation(config, expected)

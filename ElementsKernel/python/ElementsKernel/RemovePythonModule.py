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

"""
File: python/ElementsKernel/RemovePythonModule.py

Created on: 02/12/16
Author: Nicolas Morisset
"""

from __future__ import division, print_function
from future_builtins import *

import argparse
import os
import ElementsKernel.ProjectCommonRoutines as epcr
import ElementsKernel.Logging as log

logger = log.getLogger('RemovePythonModule')

################################################################################

def getAllFiles(pymodule_name, module_directory, module_name):
    """
    """
    delete_file_list=[]
    file_name_test = os.path.join(module_directory, 'tests', 'python',\
                                   pymodule_name)+ '_test.py'
    if os.path.exists(file_name_test):
        delete_file_list.append(file_name_test)
    file_name_py = os.path.join(module_directory, 'python', module_name,\
                                 pymodule_name)+ '.py'
    if os.path.exists(file_name_py):
        delete_file_list.append(file_name_py)

    return delete_file_list
           
################################################################################

def defineSpecificProgramOptions():
    description = """
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('pymodule_name', metavar='pymodule-name',
                        type=str,
                        help='Python module name')

    return parser

################################################################################

def mainMethod(args):

    logger.info('#')
    logger.info('#  Logging from the mainMethod() of the RemovePythonModule \
    script ')
    logger.info('#')

    try:
        # True: no error occured
        script_goes_on = True

        pymodule_name = args.pymodule_name

        # Default is the current directory
        module_dir = os.getcwd()

        logger.info('Current directory : %s', module_dir)

        # We absolutely need a Elements cmake file
        script_goes_on, module_name = epcr.isElementsModuleExist(module_dir)

        if script_goes_on:
            # Default is the current directory
            file_to_be_deleted = getAllFiles(pymodule_name, module_dir, module_name)
            if file_to_be_deleted:
                epcr.removeFilesOnDisk(file_to_be_deleted)
                cmakefile = os.path.join(module_dir, 'CMakeLists.txt')
                logger.warning('# !!!!!!!!!!!!!!!')
                logger.warning(' Please remove all things related to the python\
                 module name : %s ' % (pymodule_name))
                logger.warning(' in the <CMakeLists.txt> file : %s ' % (cmakefile))
                logger.warning('# !!!!!!!!!!!!!!!')
            else:
                logger.info('')
                logger.info('No file found for deletion!')
                logger.info('Script over')
        else:
            logger.error(' No module name found at the current directory : %s' % (module_dir))
            logger.error(' Script stopped...')
    except Exception as e:
        logger.exception(e)
        logger.info('# Script stopped...')
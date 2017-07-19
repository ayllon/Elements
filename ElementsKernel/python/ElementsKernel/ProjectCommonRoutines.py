"""
@file: ElementsKernel/ProjectCommonRoutines.py
@author: Nicolas Morisset

@date: 01/07/15

Purpose:
This module offers some common routines used by the Elements scripts for creating (C++, python)
projects, modules, classes etc..

@copyright: 2012-2020 Euclid Science Ground Segment

This library is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation; either version 3.0 of the License, or (at your option)
any later version.

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License
along with this library; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""

import os
import re
import shutil
import ElementsKernel.ParseCmakeLists as pcl
import ElementsKernel.ParseCmakeListsMacros as pclm
import ElementsKernel.NameCheck as nc
import ElementsKernel.Logging as log

logger = log.getLogger('ProjectCommonRoutines')

CMAKE_LISTS_FILE = 'CMakeLists.txt'

# Define exception class
class ErrorOccured(Exception):
    pass

################################################################################

def checkNameInEuclidNamingDatabase(entity_name, entity_type=""):
    """
    Check if the entity_name (e.g. project name, module name, class name etc...)
    already exists in the Euclid Naming Database. This function displays warning messages
    if the element_name exists already or the database is not available.
    """
    script_goes_on = True
    logger.info("Querying the Element Naming Database...")
    db_url = os.environ.get("ELEMENTS_NAMING_DB_URL", "")
    if not nc.checkDataBaseUrl(db_url):
        logger.info("#")
        logger.warn("!!! The Elements Naming Database URL is not valid : %s !!!", db_url)
        logger.warn("!!! Please set the ELEMENTS_NAMING_DB_URL environment variable to the Database URL !!!")
        script_goes_on = False
    else:
        info = nc.getInfo(entity_name, db_url, entity_type)
        if info["error"]:
            logger.error("There was an error querying the DB: %s", info["message"])
        else:
            if info["exists"]:
                logger.info("#")
                logger.warn("!!! The \"%s\" name for the \"%s\" type already exists in the Element Naming Database !!!",
                            entity_name, entity_type)
                logger.warn("See the result for the global query of the \"%s\" name in the DB: %s", entity_name,
                            info["url"])
                logger.warn("For more information also connect to: %s", info["private_url"])
                script_goes_on = False
            else:
                logger.warn("")
                logger.warn("The \"%s\" name of \"%s\" type doesn't exist in the Element Naming Database!!!", entity_name,
                             entity_type)
                logger.warn("Please think to add the \"%s\" name in the Element Naming Database below:", entity_name)
                logger.warn("< %s/NameCheck/project1/ >", db_url)
                logger.info("")

    if not script_goes_on:
        response_key = raw_input('Do you want to continue?(y/n, default: n)')
        if not response_key.lower() == "yes" and not response_key.lower() == "y":
                raise ErrorOccured

################################################################################

def removeFilesOnDisk(file_list):
    """
    Remove all files on hard drive from the <file_list> list.
    """
    logger.info('')
    for elt in file_list:
        logger.info('File deleted : %s', elt)
        deleteFile(elt)
    logger.info('')

################################################################################

def makeDirectory(directory_path):
    """
    Create a directory on disk if any
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
        except OSError as e:
            raise e

################################################################################

def deleteFile(path_filename):
    """
    Delete the <path_filename> file if it does exist. <path_filename> includes
    the path and filename.
    """
    if os.path.exists(path_filename):
        os.remove(path_filename)

################################################################################

def makeACopy(cmakefile):
    """
    Make a copy(backup) of the <CMakeFileLists.txt> file. The copy is named
    <CMakeFileLists.txt~>, <cmakefile> includes the path of the file.
    """
    copy_file = cmakefile + '~'
    if os.path.exists(cmakefile):
        shutil.copy(cmakefile, copy_file)
    else:
        logger.warning('File not found: <%s> Can not make a copy of this file!', cmakefile)

################################################################################

def checkNameAndVersionValid(name, version):
    """
    Check that the <name> and <version> respect a regex
    """
    name_regex = "^[A-Za-z0-9][A-Za-z0-9_-]*$"
    if not re.match(name_regex, name):
        raise ErrorOccured("Name not valid : < %s >. It must follow this regex : < %s >"
                            % (name, name_regex))

    version_regex = "^(\\d+\\.\\d+(\\.\\d+)?|HEAD)$"
    if not re.match(version_regex, version):
        raise ErrorOccured("Version number not valid : < %s >. It must follow this regex : < %s >"
                            % (version, version_regex))

################################################################################

def eraseDirectory(directory):
    """
    Erase a directory and its contents from disk
    """
    if os.path.isdir(directory):
        shutil.rmtree(directory)
        logger.info('< %s > directory erased!', directory)

################################################################################

def getAuxPathFile(file_name):
    """
    Look for the first <auxdir> path valid in the <ELEMENTS_AUX_PATH> environment
    variable where is located the <auxdir/file_name> file. It returns the
    filename with the path or an empty string if not found. We assume that the
    file_name also contains any sub directory under the <ELEMENTS_AUX_PATH>
    environment variable
    """
    found = False
    aux_dir = os.environ.get('ELEMENTS_AUX_PATH')
    file_name = file_name.replace("/", os.path.sep)
    if aux_dir is not None:
        for elt in aux_dir.split(os.pathsep):
            full_filename = os.path.join(elt, file_name)
            # look for the first valid path
            if os.path.exists(full_filename):
                found = True
                break

    if not found:
        full_filename = ''
        raise ErrorOccured("Auxiliary file not found : < %s >" % file_name)

    return full_filename

################################################################################

def copyAuxFile(destination, aux_file_name):
    """
    Copy the <aux_file_name> file to the <destination> directory.
    <aux_file_name> is just the name without path
    """
    aux_path_file = getAuxPathFile(os.path.join('ElementsKernel', 'templates', aux_file_name))
    if aux_path_file:
        shutil.copy(aux_path_file, os.path.join(destination, aux_file_name))
    else:
        raise ErrorOccured("Auxiliary file not found : < %s >" % aux_path_file)

################################################################################

def checkAuxFileExist(aux_file_name):
    """
    Make sure the <aux_file> auxiliary file exists.
    <aux_file> is just the name without the path.
    """
    auxpath = os.path.join('ElementsKernel', 'templates', aux_file_name)
    getAuxPathFile(auxpath)

################################################################################

def getAuthor():
    """
    Get the contents of the <USER> environment variables
    """
    try:
        author_str = os.environ['USER']
    except KeyError:
        author_str = ''

    return author_str

################################################################################

def checkElementsModuleNotExist(module_directory):
    """
    Get the module name in the <CMAKE_LISTS_FILE> file
    """
    module_name = ''
    cmake_file = os.path.join(module_directory, CMAKE_LISTS_FILE)
    if not os.path.isfile(cmake_file):
        raise ErrorOccured("< %s > cmake module file is missing! Are you inside a module directory?" % cmake_file)
    else:
        # Check the make file is an Elements cmake file
        # it should contain the string : "elements_project"
        f = open(cmake_file, 'r')
        for line in f.readlines():
            if 'elements_subdir' in line:
                pos_start = line.find('(')
                pos_end = line.find(')')
                module_name = line[pos_start + 1:pos_end]
        f.close()

        if not module_name:
            raise ErrorOccured("Module name not found in the <%s> file! Perhaps you are not in a " \
                                "module directory!" % cmake_file)

    return module_name

################################################################################

def checkFileNotExist(path_filename, name):
    """
    Check if the <path_filename> file does not already exist
    <path_filename> : path + filename
    """
    if os.path.exists(path_filename):
        raise ErrorOccured("File already exists there : < %s > with name : < %s >" % (path_filename, name))

################################################################################

################################################################################

def createPythonInitFile(init_path_filename):
    """
    Create on disk the __init__.py python file
    """
    if not os.path.exists(init_path_filename):
        f = open(init_path_filename, 'w')
        f.write("from pkgutil import extend_path\n")
        f.write("__path__ = extend_path(__path__, __name__)\n")
        f.close()

################################################################################

################################################################################

def updateCmakeCommonPart(cmake_filename, library_dep_list):
    """
    Update Library list in CmakeList file.
    Common code between scripts
    It returns a cmake_object object and the module name
    """
    # Backup the file
    makeACopy(cmake_filename)

    f = open(cmake_filename, 'r')
    data = f.read()
    f.close()
    cmake_object = pcl.CMakeLists(data)

    # Update find_package macro
    if library_dep_list:
        for lib in library_dep_list:
            package_object = pclm.FindPackage(lib, [])
            cmake_object.find_package_list.append(package_object)

    module_name = cmake_object.elements_subdir_list[0].name

    return cmake_object, module_name


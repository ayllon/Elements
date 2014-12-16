# -*- cmake -*-
#FindLog4CPP.cmake
#
# Created on: Jul 26, 2013
#     Author: hubert


#
# Locate log4cpp include paths and libraries
# log4cpp can be found at http://log4cpp.sourceforge.net/
# Written by Manfred Ulz, manfred.ulz_at_tugraz.at

# This module defines
# LOG4CPP_INCLUDE_DIR, where to find ptlib.h, etc.
# LOG4CPP_LIBRARIES, the libraries to link against to use pwlib.
# LOG4CPP_FOUND, If false, don't try to use pwlib.

if(NOT LOG4CPP_FOUND)


FIND_PATH(LOG4CPP_INCLUDE_DIR log4cpp/Category.hh
          PATHS "$ENV{LOG4CPP}/include" /usr/local/include /usr/include
          )

FIND_LIBRARY(LOG4CPP_LIBRARIES log4cpp
            PATHS "$ENV{LOG4CPP}/lib" /usr/local/lib /usr/lib
            )

set(LOG4CPP_INCLUDE_DIRS ${LOG4CPP_INCLUDE_DIR})

# handle the QUIETLY and REQUIRED arguments and set LOG4CPP_FOUND to TRUE if
# all listed variables are TRUE
  INCLUDE(FindPackageHandleStandardArgs)
  FIND_PACKAGE_HANDLE_STANDARD_ARGS(Log4CPP DEFAULT_MSG LOG4CPP_INCLUDE_DIR LOG4CPP_LIBRARIES)

  mark_as_advanced(LOG4CPP_FOUND LOG4CPP_INCLUDE_DIR LOG4CPP_LIBRARIES)

endif()

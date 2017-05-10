'''
Created on May 10, 2017

@author: Hubert Degaudenzi

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

'''
import unittest

from ElementsKernel.Program import Program

class ProgramTestTest(unittest.TestCase):


    def testConstructor(self):
        # The following lines should not raise any exception
        p = Program("ElementsExamples.PythonProgramExample")
        p2 = Program("ElementsExamples.PythonProgramExample", original_path="")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testConstructor']
    unittest.main()

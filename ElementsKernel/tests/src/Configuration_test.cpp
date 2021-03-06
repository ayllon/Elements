/**
 * @file Configuration_test.cpp
 *
 * Created on: Dec 4, 2013
 *     Author: Pierre Dubath
 *
 * @copyright 2012-2020 Euclid Science Ground Segment
 *
 * This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General
 * Public License as published by the Free Software Foundation; either version 3.0 of the License, or (at your option)
 * any later version.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 *
 */

#include "ElementsKernel/Configuration.h"  // header to test

#include <algorithm>  // for for_each, transform, copy_if
#include <string>     // for std::string
#include <vector>     // for std::vector

#include <boost/filesystem/fstream.hpp>     // for ofstream
#include <boost/filesystem/operations.hpp>  // for exists
#include <boost/test/unit_test.hpp>         // for boost unit test macros

#include "ElementsKernel/Path.h"       // for joinPath, Item
#include "ElementsKernel/System.h"     // for DEFAULT_INSTALL_PREFIX
#include "ElementsKernel/Temporary.h"  // for TempDir, TempEnv
#include <ElementsKernel/Exception.h>  // for Exception

using std::string;
using std::vector;

using boost::filesystem::exists;
using boost::filesystem::is_regular;

namespace Elements {

//-----------------------------------------------------------------------------

//-----------------------------------------------------------------------------
//
// Begin of the Boost tests
//
//-----------------------------------------------------------------------------

struct Configuration_Fixture {

  TempDir            m_top_dir;
  vector<Path::Item> m_item_list;
  vector<Path::Item> m_target_item_list;
  vector<Path::Item> m_real_item_list;
  vector<Path::Item> m_target_real_item_list;

  Configuration_Fixture() : m_top_dir{"Configuration_test-%%%%%%%"} {

    using std::copy_if;
    using std::distance;
    using std::for_each;

    m_item_list.emplace_back(m_top_dir.path() / "test1");
    m_item_list.emplace_back(m_top_dir.path() / "test1" / "foo");
    m_item_list.emplace_back(m_top_dir.path() / "test2");
    m_item_list.emplace_back(m_top_dir.path() / "test3");

    for_each(m_item_list.cbegin(), m_item_list.cend(), [](Path::Item p) {
      boost::filesystem::create_directory(p);
    });

    m_item_list.emplace_back(m_top_dir.path() / "test4");

    m_target_item_list = m_item_list;

    m_target_item_list.emplace_back(Path::Item(System::DEFAULT_INSTALL_PREFIX) / "share" / "conf");

    m_real_item_list.resize(m_item_list.size());
    auto it = copy_if(m_item_list.begin(), m_item_list.end(), m_real_item_list.begin(), [](const Path::Item& p) {
      return exists(p);
    });
    m_real_item_list.erase(it, m_real_item_list.end());

    m_target_real_item_list.resize(m_target_item_list.size());
    auto it2 = copy_if(m_target_item_list.begin(), m_target_item_list.end(), m_target_real_item_list.begin(),
                       [](const Path::Item& p) {
                         return exists(p);
                       });
    m_target_real_item_list.erase(it2, m_target_real_item_list.end());
  }

  ~Configuration_Fixture() {}
};

BOOST_AUTO_TEST_SUITE(Configuration_test)

//-----------------------------------------------------------------------------

BOOST_AUTO_TEST_CASE(ConfigurationException_test) {

  BOOST_CHECK_THROW(getConfigurationPath("NonExistingFile.conf"), Exception);
}

BOOST_AUTO_TEST_CASE(ConfigurationVariableName_test) {

  BOOST_CHECK_EQUAL(getConfigurationVariableName(), "ELEMENTS_CONF_PATH");
}

BOOST_FIXTURE_TEST_CASE(getFromLocations_test, Configuration_Fixture) {

  auto env = TempEnv();

  env["ELEMENTS_CONF_PATH"] = Path::join(m_item_list);

  auto locations = getConfigurationLocations();

  BOOST_CHECK_EQUAL_COLLECTIONS(locations.begin(), locations.end(), m_target_item_list.begin(),
                                m_target_item_list.end());
}

BOOST_FIXTURE_TEST_CASE(getFromLocationsExist_test, Configuration_Fixture) {

  auto env = TempEnv();

  env["ELEMENTS_CONF_PATH"] = Path::join(m_real_item_list);

  auto locations = getConfigurationLocations(true);

  BOOST_CHECK_EQUAL_COLLECTIONS(locations.begin(), locations.end(), m_target_real_item_list.begin(),
                                m_target_real_item_list.end());
}

BOOST_AUTO_TEST_SUITE_END()

//-----------------------------------------------------------------------------
//
// End of the Boost tests
//
//-----------------------------------------------------------------------------

}  // namespace Elements

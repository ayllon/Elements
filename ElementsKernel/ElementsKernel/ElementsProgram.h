/**
 * @file ElementsProgram.h
 * 
 * Created on: Jul 18, 2013
 * 
 * @author Pierre Dubath
 *
 */

#ifndef ELEMENTSPROGRAM_H_
#define ELEMENTSPROGRAM_H_

#include <boost/filesystem.hpp>
#include <boost/program_options.hpp>
#include "ElementsKernel/ElementsLogging.h"

/**
 * Macro which must be used to create a main in classes
 * that derived from ElementsProgram, i.e., these derived classes
 * must end with the following line:
 * 		BUILD_MAIN_FOR(ElementsProgramExample)
 */
#define BUILD_MAIN_FOR(ElementsProgramName) 		\
  int main(int argc, char** argv) 					\
  {                               					\
    ElementsProgramName elementProgramInstance {} ;	\
    return elementProgramInstance.run(argc, argv) ;	\
  }

/**
 * @class ElementsProgram
 * @brief
 * 		Base class for all Element programs
 * @details
 * 		This base class takes care of program options and of logging
 * 		initialization. All Elements program extending this class
 */
class ElementsProgram {
public:
	int run(int argc, char* argv[]);

protected:
	ElementsProgram();
	virtual ~ElementsProgram();

	/**
	 * The pseudo main that all programs must implement.
	 */
	virtual int pseudoMain() = 0;

	virtual boost::program_options::options_description defineSpecificProgramOptions() = 0;

	virtual std::string getVersion() = 0;

	const boost::program_options::variables_map& getVariablesMap() const {
		return m_variablesMap;
	}

private:

	const boost::filesystem::path getDefaultConfigFile(
			std::string programName) const;
	const boost::filesystem::path getDefaultLogFile(
			std::string programName) const;

	const boost::program_options::variables_map getProgramOptions(int argc,
			char* argv[]);

	void logAllOptions(std::string programName);

	boost::filesystem::path m_logFile;
	/**
	 * This is the BOOST program options variable_map used to store all program options
	 */
	boost::program_options::variables_map m_variablesMap { };

};

#endif /* ELEMENTSPROGRAM_H_ */

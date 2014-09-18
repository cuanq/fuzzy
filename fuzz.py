"""
File: fuzz.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
# Import sys and parseargs for input reading
import parseargs
import sys

# Import Discover and Auth for handling input
import Discover, Auth

class Fuzz:
	parser = argparse.ArgumentParser( description = 'Fuzzer for website security testing.' )
	parser.add_argument( 'command', type = string, help = 'Direct the Fuzzer\'s actions to:\n\t\'Discover\'\t- Output a comprehensive, human-readable list of all discovered inputs to the system. Techniques include both crawling and guessing.\n\t\'Test\'\t- Discover all inputs, then attempt a list of exploit vectors on those inputs. Report potential vulnerabilities.' )
	parser.add_argument( 'url', type = string, help = 'URL where the fuzzer should begin its search.' )
	parser.add_argument( '--custom-auth', dest = 'custom-auth', help = 'Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa).' )
	parser.add_argument( '--common-words', dest = 'common-words', help = 'Newline-delimited file of common words to be used in page guessing and input guessing.' )
	parser.add_argument( '--vectors', dest = 'vectors', help = 'Newline-delimited file of common exploits to vulnerabilities.' )
	parser.add_argument( '--sensitive', dest = 'sensitive', help = 'Newline-delimited file data that should never be leaked.' )
	parser.add_argument( '--random', dest = 'random', help = 'When off, try each input to each page systematically.  When on, choose a random page, then a random input field and test all vectors. Default: False.' )
	parser.add_argument( '--slow', dest = 'slow', help = 'Number of milliseconds considered when a response is considered "slow". Default is 500 milliseconds.' )
	args = parser.parse_args()

	


if __name__ == '__main__':
	Fuzz()
"""
File: fuzz.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
# Import sys and parseargs for input reading
import argparse
import sys

# Import Beautiful Soup for web scraping
from bs4 import BeautifulSoup

# Import Discover and Auth for handling input
import discovery

def main():
	parser = argparse.ArgumentParser( description = 'Fuzzer for website security testing.' )

	parser.add_argument( 'fuzzer-action', nargs = '?', 
		help = 'Direct the Fuzzer\'s actions to:\'discover\' - Output a comprehensive, human-readable list of all discovered inputs to the system. Techniques include both crawling and guessing.\'test\' - Discover all inputs, then attempt a list of exploit vectors on those inputs. Report potential vulnerabilities. This argument is Required.' )
	
	parser.add_argument( 'url', nargs = '?', 
		help = 'URL where the fuzzer should begin its search. This argument is Required.' )
	
	parser.add_argument( '--custom-auth', dest = 'custom-auth', 
		help = 'Signal that the fuzzer should use hard-coded authentication for a specific application (e.g. dvwa).' )
	
	parser.add_argument( '--common-words', dest = 'common-words', 
		help = 'Newline-delimited file of common words to be used in page guessing and input guessing. This argument is Required.' )
	
	args = vars( parser.parse_args() )

	""" Make sure that required arguments are present """
	if args['fuzzer-action'] == 'discover':
		if args['url'] == None:
			print( 'Must specify a url to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
			sys.exit()
		
		if args['common-words'] == None:
			print( 'Must specify a common-words file to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
			sys.exit()
	elif args['fuzzer-action'] == 'test':
		print( 'Test functionality will be available in Release 2. Use \'python fuzz.py -h\' for more help.' )
		sys.exit()
	else:
		print( 'Must specify either \'Discover\' or \'Test\' for the fuzzer action. Use \'python fuzz.py -h\' for more help.' )
		sys.exit()


	""" Handle the given arguments based on the action """
	# Create lists from discovered links
	session = requests.Session()
	discovered_links	= discovery.discoverLink( args['url'] )
	guessed_links		= discovery.guessPage( args['url'], args['common-words'], discovered_links, session )

	# Merge the two lists for a full link array
	all_links			= discovered_links + guessed_links

	if args['fuzzer-action'] == 'discover':
		discoverPrintOut( discovered_links, guessed_links )

	else: # fuzzer action == 'test' from earlier check
		pass



def discoverPrintOut( discovered_links, guessed_links ):
	print_input = raw_input( 'Discovery completed. Would you like the discovered links printed to:\n\t[d] - Document\n\t[t] - Terminal\n\t[b] - Both document and terminal\n\t[n] - Not Printed\nPrinting to document will overwrite previous printings.\nInput: ' )

	if print_input == 't':
		print( 'Discover Printout:\n' )

		print( '\t- Discovered Links -\n' )
		for link in discovered_links:
			print( link + '\n' )

		print( '\n\t- Guessed Links -\n' )
		for link in guessed_links:
			print( link + '\n' )

	elif print_input == 'd':
		discoveryFile = open( 'discovery_output.txt', 'w+' )
		discoveryFile.write( 'Discover Printout:\n' )
		discoveryFile.write( '\t- Discovered Links -\n' )
		for link in discovered_links:
			discoveryFile.write( link + '\n' )
		discoveryFile.write( '\n\t- Guessed Links -\n' )
		for link in guessed_links:
			discoveryFile.write( link + '\n' )
		

	elif print_input == 'b':
		print( 'file output is not yet implemented. Terminal output:' )

		print( 'Discover Printout:\n' )

		print( '\t- Discovered Links -\n' )
		for link in discovered_links:
			print( link + '\n' )

		print( '\n\t- Guessed Links -\n' )
		for link in guessed_links:
			print( link + '\n' )


		discoveryFile = open( 'discovery_output.txt', 'w+' )
		discoveryFile.write( 'Discover Printout:\n' )
		discoveryFile.write( '\t- Discovered Links -\n' )
		for link in discovered_links:
			discoveryFile.write( link + '\n' )
		discoveryFile.write( '\n\t- Guessed Links -\n' )
		for link in guessed_links:
			discoveryFile.write( link + '\n' )
	elif print_input == 'n':
		pass

	else:
		print( 'Invalid Input. Closing Fuzzer.' )
		sys.exit()

	print( 'Fuzzer Discovery completed.' )


if __name__ == '__main__':
	main()





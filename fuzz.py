"""
File: fuzz.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
# Import sys and parseargs for input reading
import argparse
import sys
from custom_auth import *

# Import Beautiful Soup for web scraping
from bs4 import BeautifulSoup

# Import requests for handling website
import requests

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
			
		if args['custom-auth'] == 'dvwa':
			payload = {
				"username": custom_auth[args['custom-auth']]["username"],
				"password": custom_auth[args['custom-auth']]["password"],
				"login": "login"
			}
			session = requests.Session()
			session.post(custom_auth[args['custom-auth']]["login_url"], data=payload)			
			page = session.get(args['url'] + "/" + args['custom-auth'])
			
		elif args['custom-auth'] == 'bodgeit':
			session = requests.Session()
			page = session.get(custom_auth[args['custom-auth']]["login_url"])
			
		else:
			session = requests.Session()
			page = session.get(args['url'])
		
	elif args['fuzzer-action'] == 'test':
		print( 'Test functionality will be available in Release 2. Use \'python fuzz.py -h\' for more help.' )
		sys.exit()
	else:
		print( 'Must specify either \'Discover\' or \'Test\' for the fuzzer action. Use \'python fuzz.py -h\' for more help.' )
		sys.exit()
		
	""" Handle the given arguments based on the action """
	# Create lists from discovered links
	discovered_links	= discovery.discoverLink( args['url'] )
	guessed_links		= discovery.guessPage( page, args['common-words'], discovered_links, session)

	# Merge the two lists for a full link array
	all_links = discovered_links + guessed_links
	input_list = []
	if args['fuzzer-action'] == 'discover':
		discoverPrintOut( discovered_links, guessed_links )

		input_list = discovery.parseURL(all_links)
		inputPrintOut( input_list )

	else: # fuzzer action == 'test' from earlier check
		pass

def discoverPrintOut( discovered_links, guessed_links ):
	print_input = input( 'Discovery completed. Would you like the discovered links printed to:\n\t[d] - Document\n\t[t] - Terminal\n\t[b] - Both document and terminal\n\t[n] - Not Printed\nPrinting to discovery document will overwrite previous printings.\nInput: ' )

	if print_input == 't':
		print( 'Discover Printout:\n' )

		print( '\t- Discovered Links -\n' )
		for link in discovered_links:
			try:
				print(link + '\n')
			except:
				print('LINK REMOVED: Improper characterization of text.\n')
		print( '\n\t- Guessed Links -\n' )
		for link in guessed_links:
			print( link + '\n' )

		print( 'Printed to Terminal. ' )

	elif print_input == 'd':
		discoveryFile = open( 'discovery_output.txt', 'w+' )
		discoveryFile.write( 'Discover Printout:\n' )
		discoveryFile.write( '\t- Discovered Links -\n' )
		for link in discovered_links:
			discoveryFile.write( link + '\n' )
		discoveryFile.write( '\n\t- Guessed Links -\n' )
		for link in guessed_links:
			discoveryFile.write( link + '\n' )

		print( 'Printed to discovery_output.txt. ' )

	elif print_input == 'b':
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

		print( 'Printed to both Terminal and discovery_output.txt. ' )

	elif print_input == 'n':
		pass

	else:
		print( 'Invalid Input. Closing Fuzzer.' )
		sys.exit()

	print( 'Fuzzer Discovery completed.\n' )


def inputPrintOut( input_list ):
	print_input = input( 'Input Parsing completed. Would you like the discovered inputs printed to:\n\t[d] - Document\n\t[t] - Terminal\n\t[b] - Both document and terminal\n\t[n] - Not Printed\nPrinting to input document will overwrite previous printings.\nInput: ' )

	if print_input == 't':
		print( 'Input Parsing Printout:\n' )

		print( '\t- Input -\n' )
		for this_input in input_list:
			try:
				print(this_input + '\n')
			except:
				print('INPUT REMOVED: Improper characterization of text.\n')

		print( 'Printed to Terminal. ' )

	elif print_input == 'd':
		inputsFile = open( 'inputs_output.txt', 'w+' )
		inputsFile.write( 'Input Parsing Printout:\n' )
		discoveryFile.write( '\t- Input -\n' )
		for this_input in input_list:
			inputsFile.write( this_input + '\n' )

		print( 'Printed to inputs_output.txt. ' )

	elif print_input == 'b':
		print( 'Input Parsing Printout:\n' )

		print( '\t- Input -\n' )
		for this_input in input_list:
			try:
				print(this_input + '\n')
			except:
				print('INPUT REMOVED: Improper characterization of text.\n')

		inputsFile = open( 'inputs_output.txt', 'w+' )
		inputsFile.write( 'Input Parsing Printout:\n' )
		inputsFile.write( '\t- Input -\n' )
		for this_input in input_list:
			inputsFile.write( this_input + '\n' )

		print( 'Printed to Terminal and inputs_output.txt. ' )

	else:
		print( 'Invalid Input. Closing Fuzzer.' )
		sys.exit()

	print( 'Fuzzer Input Parsing completed.\n' )


if __name__ == '__main__':
	main()





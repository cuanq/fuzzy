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

	parser.add_argument( '--vectors', dest = 'vectors',
		help = 'Newline-delimited file of common exploits to vulnerabilities. Required.' )

	parser.add_argument( '--sensitive', dest = 'sensitive',
		help = 'Newline-delimited file data that should never be leaked. It\'s assumed that this data is in the application\'s database (e.g. test data), but is not reported in any response. Required.' )

	parser.add_argument( '--random', dest = 'random',
		help = 'When off, try each input to each page systematically.  When on, choose a random page, then a random input field and test all vectors. Default: false.' )

	parser.add_argument( '--slow', dest = 'slow',
		help = 'Number of milliseconds considered when a response is considered "slow". Default is 500 milliseconds.' )
	
	args = vars( parser.parse_args() )

	""" Make sure that required arguments are present """
	if args['fuzzer-action'] == 'discover':
		if args['url'] == None:
			print( 'Must specify a url to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
			sys.exit()
		
		if args['common-words'] == None:
			print( 'Must specify a common-words file to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
			sys.exit()

		session = requests.Session()
		page = session.get( args['url'] )
			
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
	
	input_list = discovery.parseURL(all_links)

	if discovery.discoverCookie(session) == False:
		print( '\nWe have cookies too!' )

	form_params = list()
	for link in all_links:
		""" Create page from link variable """
		session = requests.Session()
		this_page = session.get(link)
		form_params.append(discovery.formParams(this_page))

	""" What to do with gathered information from discovery """
	if args['fuzzer-action'] == 'discover':
		print_input = discoverPrintOut( discovered_links, guessed_links )
		inputPrintOut( input_list, print_input )
		paramPrintOut( form_params, print_input )

	else:
		""" fuzzer-action == 'test' """
		pass


def discoverPrintOut( discovered_links, guessed_links ):
	print_input = input( 'Discovery completed.\n\nWould you like the results of the Fuzzing printed to:\n\t[d] - Document\n\t[t] - Terminal\n\t[b] - Both document and terminal\n\t[n] - Not Printed\nPrinting to discovery document will overwrite previous printings.\nInput: ' )

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

		print( 'Discovery Printed to Terminal. ' )

	elif print_input == 'd':
		discoveryFile = open( 'discovery_output.txt', 'w+' )
		discoveryFile.write( 'Discover Printout:\n' )
		discoveryFile.write( '\t- Discovered Links -\n' )
		for link in discovered_links:
			discoveryFile.write( link + '\n' )
		discoveryFile.write( '\n\t- Guessed Links -\n' )
		for link in guessed_links:
			discoveryFile.write( link + '\n' )

		print( 'Discovery Printed to discovery_output.txt. ' )

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

		print( 'Discovery Printed to both Terminal and discovery_output.txt. ' )

	elif print_input == 'n':
		print( 'Did not print discovery.\n' )

	else:
		print( 'Invalid Input. Closing Fuzzer.' )
		sys.exit()

	print( 'Fuzzer Discovery completed.\n' )
	return print_input


def inputPrintOut( input_list, print_input ):
	if print_input == 't':
		print( 'Input Parsing Printout:\n' )

		print( '\t- Input -\n' )
		for this_input in input_list:
			try:
				print(this_input + '\n')
			except:
				print('INPUT REMOVED: Improper characterization of text.\n')

		print( 'Input Printed to Terminal. ' )

	elif print_input == 'd':
		inputsFile = open( 'inputs_output.txt', 'w+' )
		inputsFile.write( 'Input Parsing Printout:\n' )
		inputsFile.write( '\t- Input -\n' )
		for this_input in input_list:
			inputsFile.write( this_input + '\n' )

		print( 'Input Printed to inputs_output.txt. ' )

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

		print( 'Input Printed to Terminal and inputs_output.txt. ' )

	else:
		print( 'Did not print Input.\n' )

	print( 'Fuzzer Input Parsing completed.\n' )

def paramPrintOut( form_params, print_input ):
	if print_input == 't':
		print( 'Form Param Printout:\n' )
		print( '\t- Form Params -\n' )
		for param in form_params:
			this_type = param[0]['type']
			this_name = param[0]['name']
			print( 'Input Type: ' + this_type + ', Input Name: ' + this_name + '\n' )
		print( 'Form Params printed to Terminal.' )

	elif print_input == 'd':
		paramsFile = open( 'params_output.txt', 'w+' )
		paramsFile.write( 'Form Param Printout:\n' )
		paramsFile.write( '\t- Form Params -\n' )
		for param in form_params:
			this_type = param[0]['type']
			this_name = param[0]['name']
			paramsFile.write( 'Input Type: ' + this_type + ', Input Name: ' + this_name + '\n' )

		print( 'Form Params printed to params_output.txt' )

	elif print_input == 'b':
		print( 'Form Param Printout:\n' )
		print( '\t- Form Params -\n' )
		for param in form_params:
			this_type = param[0]['type']
			this_name = param[0]['name']
			print( 'Input Type: ' + this_type + ', Input Name: ' + this_name + '\n' )

		paramsFile = open( 'params_output.txt', 'w+' )
		paramsFile.write( 'Form Param Printout:\n' )
		paramsFile.write( '\t- Form Params -\n' )
		for param in form_params:
			this_type = param[0]['type']
			this_name = param[0]['name']
			paramsFile.write( 'Input Type: ' + this_type + ', Input Name: ' + this_name + '\n' )

		print( 'Form Params Printed to Terminal and params_output.txt. ' )

	else:
		print( 'Did not print Form Params.' )

	print( 'Fuzzer Form Params completed.' )

if __name__ == '__main__':
	main()





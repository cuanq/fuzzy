"""
File: fuzz.py
Authors: Zack Downs <zjd2035@gmail.com>, Danielle Gonzalez <dng2551@rit.edu>, Stephan Wlodarczyk <stephanjwlodarczyk@gmail.com>
"""
# Import sys and parseargs for input reading
import argparse
import sys
from custom_auth import *
from collections import defaultdict

# Import Beautiful Soup for web scraping
from bs4 import BeautifulSoup

# Import requests for handling website
import requests

# Import Discover and Auth for handling input
import discovery

# Import Test for fuzz testing
import test

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

	if args['url'] == None:
		print( 'Must specify a url to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
		sys.exit()
		
	if args['common-words'] == None:
		print( 'Must specify a common-words file to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
		sys.exit()

	""" Make sure that required arguments are present """
	if args['fuzzer-action'] == 'discover':
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
		if args['vectors'] == None:
			print( 'Must specify a vectors file to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
			sys.exit()

		if args['sensitive'] == None:
			print( 'Must specify a sensitive file to begin fuzzing. Use \'python fuzz.py -h\' for more help.' )
			sys.exit()

		if args['random'] == None:
			args['random'] = "False"

		if args['slow'] == None:
			args['slow'] = 500
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

	form_dict = list()
	for link in all_links:
		""" Get all forms from links """
		forms = discovery.formParams(link)
		for form in forms:
			form_dict.append( form )

	""" What to do with gathered information from discovery """
	if args['fuzzer-action'] == 'discover':
		print_input = discoverPrintOut( discovered_links, guessed_links )
		inputPrintOut( input_list, print_input )
		paramPrintOut( form_dict, print_input )

	else:
		""" fuzzer-action == 'test' """
		# Send arguments to necessary testing file, where files can be retrieved
		test.test_pages( form_dict, args )


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

""" MUST REHANDLE PRINTOUT OF FORMS """
def formsPrintOut( forms, print_input ):
	if print_input == 't':
		print( 'Form Printout:\n' )
		print( '\t- Forms -\n' )
		for form in forms:
			form_name = form['name']
			print( 'Form Name: ' + form_name + '\n' )
		print( 'Forms printed to Terminal.' )

	elif print_input == 'd':
		formsFile = open( 'forms_output.txt', 'w+' )
		formsFile.write( 'Form Printout:\n' )
		formsFile.write( '\t- Forms -\n' )
		for form in forms:
			form_name = form['name']
			formsFile.write( 'Form Name:' + form_name + '\n' )

		print( 'Forms printed to forms_output.txt' )

	elif print_input == 'b':
		print( 'Form Printout:\n' )
		print( '\t- Forms -\n' )

		formsFile = open( 'forms_output.txt', 'w+' )
		formsFile.write( 'Form Printout:\n' )
		formsFile.write( '\t- Forms -\n' )

		for form in forms:
			form_name = form['name']
			print( 'Form Name: ' + form_name + '\n' )
			formsFile.write( 'Form Name: ' + form_name + '\n' )

		print( 'Forms Printed to Terminal and forms_output.txt. ' )

	else:
		print( 'Did not print Forms.' )

	print( 'Fuzzer Form Scanning completed.' )

if __name__ == '__main__':
	main()





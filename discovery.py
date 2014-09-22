# for getting and parsing web pages 
import requests
import custom_auth
from urlparse import urljoin 
from urlparse import urlparse
#from urllib.parse import urljoin
#from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Fuzzer should keep a list of URLs that it can reach from init page
# no off-site links
def discoverLink(page):
	linksFound = []

	parsed_url = urlparse(page)
	site = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)

	aPage = requests.get(page)
	pageData = aPage.text
	pageSoup = BeautifulSoup(pageData)
	for link in pageSoup.find_all('a'):
		if (link.get('href')).startswith(site):
			linksFound.append(link.get('href'))
		else:
			linksFound.append(site + link.get('href'))

	return linksFound

# Fuzzer should use common word list to discover potentially unlinked pages
def guessPage(page, commonFile, linksFound, session):
	guessed_pages = []
	common_words = open(commonFile, "r+").read().splitlines()
	common_extent = open("commonExtensions.txt").read().splitlines()
	print('\n###3###\n')
	for word in common_words:
		for extent in common_extent:
			pageGuess = session.get(page.url + word + "." + extent)
			if pageGuess.status_code < 300 and pageGuess.url not in linksFound:
				guessed_pages.append(pageGuess)
	return guessed_pages

def parseURL(page):

	# empty list for any inputs found
	inputs_found = []

	# get the links 
	pageLinks = discoverLink(page)

	#get the base site, as done in discoverLink

	parsed_url = urlparse(page)
	baseSite = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
	# get the guessed links? 
	# guessLinks = guessPage(page, commonFile, pageLinks)

	for link in pageLinks:
		if link.startswith(baseSite):
			parsed_link = urlparse(link)	#this lets us pull out the query from individual links
			inputs_found.append(parsed_link.query) #put these inputs in a list 

	return inputs_found




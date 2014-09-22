# for getting and parsing web pages 
import requests
import custom_auth
from urllib.parse import urljoin
from urllib.parse import urlparse
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
	for word in common_words:
		for extent in common_extent:
			pageGuess = session.get(page.url + word + "." + extent)
			if pageGuess.status_code < 300 and pageGuess.url not in linksFound:
				guessed_pages.append(pageGuess)
	return guessed_pages

def parseURL(all_Links):

	# empty list for any inputs found
	inputs_found = []


	for link in all_Links:
		parsed_link = urlparse(link)	# this lets us pull out the query from individual links
		this_query = parsed_link.query
		if this_query != '':
			print(this_query)
			#inputs_found.append(this_query) # put these inputs in a list 
	return inputs_found


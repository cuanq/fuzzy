# for getting and parsing web pages 
import requests
import custom_auth
from urllib.parse import urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict

# Fuzzer should keep a list of URLs that it can reach from init page
# no off-site links
def discoverLink(page):
	linksFound = []

	parsed_url = urlparse(page)
	site = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)

	aPage = requests.get(page)
	pageData = aPage.text
	pageSoup = BeautifulSoup(pageData)
	"""for link in pageSoup.find_all('a'):
		linksFound.append(link.get('href'))"""
	for link in pageSoup.find_all('a'):
		if (link.get('href')).startswith(site):
			linksFound.append(link.get('href'))
		else:
			if (link.get('href').startswith('http://')):
				pass
			else:
				linksFound.append(site + '/' + link.get('href'))

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
				guessed_pages.append(pageGuess.url)
	return guessed_pages

def parseURL(all_Links):

	# empty list for any inputs found
	inputs_found = []


	for link in all_Links:
		parsed_link = urlparse(link)	# this lets us pull out the query from individual links
		this_query = parsed_link.query
		if this_query != '':
			#print(this_query)
			inputs_found.append(this_query) # put these inputs in a list 
	return inputs_found

def discoverCookie(session):
	#if 'htttp://127.0.0.1/dvwa/login.php' in page.url and 'logout.php' not in url and auth == #'dvwa': page, session = dvwa_relogin(session, page.url)
	cookies = session.cookies
	
	#empty list for any cookies found
	cookie_jar = []
	isCookieJarEmpty = True;
	
	#find some cookies; if found, store in jar
	for cookie in cookies:
		i_has_cookie = {"name": cookie.name, "value": cookie.value}
		cookie_jar.append(i_has_cookie)
	
	if len(cookie_jar) > 0:
		isCookieJarEmpty = False;
	
	return isCookieJarEmpty

def formParams(link):
	session = requests.Session()
	page = session.get(link)
	pageSoup = BeautifulSoup(page.content)

	forms = list()

	for form in pageSoup.find_all('form'):
		form_dict = {'url':link, 'action':'', 'name':'', 'method':'', 'inputs': list()}

		if form.has_attr('name'):
			form_dict['name'] = form['name']

		if form.has_attr('action') and form.has_attr('method'):
			form_dict['action'] = form['action']
			form_dict['method'] = form['method']

			for form_field in form.find_all('input'):
				if form_field.has_attr('name'):
					form_dict['inputs'].append(form_field['name'])

			forms.append(form_dict)

	return form_dict












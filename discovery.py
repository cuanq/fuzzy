# for getting and parsing web pages 
import requests
# from urlparse import urljoin (these imports 
# from urlparse import urlparse
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

# Fuzzer should use common word list to discover potenially unlinked pages
def guessPage(page, commonFile, linksFound, session):
    guessed_pages = []
    common_words = open(commonFile, "r").read().splitlines()
    common_extent = open("commonExtensions.txt").read().splitlines()

    for word in common_words:
        for extent in common_extent:
            pageGuess = session.get(page + word + "." + extent)

            # if it exists and isn't in linksFound, add to guessed_pages 
            # check session code 
            if pageGuess < 300 and pageGuess.url not in linksFound:
                guessed_pages.append(pageGuess)

    
    return guessed_pages



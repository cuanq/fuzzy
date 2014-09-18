# for getting and parsing web pages 
import requests
from urlparse import urljoin
from urlparse import urlparse
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
def guessPage():
    pass
#
# Simple web crawler
#

# TODO:
# 1. Break more links are available
# 2. Try to avoid duplicatate links responses
# 3. Try to draft a simple site(pages) to debug the crawler

# import libraries
import json
import requests
from bs4 import BeautifulSoup

#start_url = 'http://quotes.toscrape.com'
start_url = 'https://code-monkey-king.herokuapp.com'

data = []

def crawl(url, depth):
    try:
        print('Crawling url: "%s" at depth: %d' % (url, depth))
        response = requests.get(url)
    except:
        print('Failed to perform HTTP GET request on "%s"\n' % url)
        return
    
    content = BeautifulSoup(response.text, 'lxml')

    title = content.find('title').text
    description = content.get_text()
    
    if description is None:
        description = ''
    else:
        description = description.strip().replace('\n', ' ')
    
    result = {
        'url': url,
        'title': title,
        'description': description
    }
    
    data.append(result)
    
    # return when depth is exhausted
    if depth == 0:
        return

    try:
        links = content.findAll('a')
    except:
        return

    for link in links:
        try:
            if 'http' not in link['href']:
                follow_url = url + link['href']
            else:
                follow_url = link['href']

            crawl(follow_url, depth - 1)
        except KeyError:
            pass
    
    return

crawl(start_url, 2)
print(len(data))





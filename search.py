import requests

"""page =('<div id="top_bin"><div id="top_content" class="width960">'
       '<div class="udacity float-left"><a href="http://udacity.com">')
"""

#Get the webpage content
def get_page(website_url):
    response = requests.get(website_url)
    return response.content
#Get the next URL in the page
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None,0
    else:
        start_quote = page.find('\"',start_link)
        end_quote = page.find('\"',start_quote+1)
        url = page[start_quote+1:end_quote]
        return url, end_quote

#Print all the urls in a page
def print_all_links(page):
    while True:
        url, end_pos = get_next_target(page)
        if url:
            print url
            page = page[end_pos+1:]
        else:
            break
#Get all the urls in a page
def get_all_links(page):
    links = []
    while True:
        url, end_pos = get_next_target(page)
        if url:
            links.append(url)
            page = page[end_pos+1:]
        else:
            break
    return links

#print get_all_links(get_page('http://www.udacity.com/cs101x/index.html'))
#print_all_links(get_page('http://xkcd.com/353'))

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
    
#Crawl the web
def crawl(seed):
    tocrawl = [seed]
    crawled = []
    while tocrawl:
        url = tocrawl.pop()
        if url not in crawled:
            union(tocrawl,get_all_links(get_page(url)))
            crawled.append(url)
    return crawled

print crawl('http://www.udacity.com/cs101x/index.html')
#print crawl('http://xkcd.com/353')


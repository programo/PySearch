import requests
import urllib

#Get the webpage content
def get_page(url):
    try:
        response = requests.get(url)
        return response.content
    except:
        return ""

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

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

#Add to index 

"""
index datastructure is a  python dictionary  {keyword1 : [url1,url2,..],
                                                keyword2 : [url1,url2,..],
                                                }
"""
def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

#A look up for the index
def look_up(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

#Add a page to index
def add_page_to_index(index,url,page_content):
    content_list = page_content.split()
    for word in content_list:
        add_to_index(index,word,url)

##Crawl the web and return the index
def crawl(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}
    while tocrawl:
        url = tocrawl.pop()
        if url not in crawled:
            contents = get_page(url)
            add_page_to_index(index,url,contents)
            outlinks = get_all_links(contents)
            graph[url] = outlinks
            union(tocrawl,outlinks)
            crawled.append(url)
    return index, graph

index, graph = crawl('http://udacity.com/cs101x/urank/index.html')

#Compute ranks
def compute_ranks(graph):
    d = 0.8 #damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages #The default rank of each page
    for i in range(0,numloops):
        newranks = {}
        for page in graph:
            newrank  = (1 - d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + (d * ranks[node]) / len(graph[node])
            newranks[page] = newrank
        ranks = newranks
    return ranks

#Search Engine

def search(index, ranks, keyword):
    



#index, graph = crawl('http://www.udacity.com/cs101x/index.html')

print compute_ranks(graph)
#print crawl('http://xkcd.com/353')
#print index
#print look_up(index,'<html>')


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

#print get_all_links(get_page('http://www.udacity.com/cs101x/index.html'))
#print_all_links(get_page('http://xkcd.com/353'))

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
    
#Add to index 

"""
index datastructure
index = [[keyword1,[url1,url2,...]],[keyword2,[url1,url2,...]],...]

"""
def add_to_index(index,keyword,url):
    for x in index:
        if keyword == x[0]:
            #Check if the url is already present for that particular keyword
            if url in x[1]:
                return
            else:
                x[1].append(url)
                return
    index.append([keyword,[url]])

#add_to_index(index,'udacity','http://udacity.com')
#add_to_index(index,'computing','http://acm.org')
#add_to_index(index,'udacity','http://npr.org')
#print index

#A look up for the index
def look_up(index, keyword):
    for x in index:
        if x[0] == keyword:
            return x[1]
    return []

#print look_up(index,'udacity')
#print look_up(index,'aswin')




#Add a page to index
def add_page_to_index(index,url,page_content):
    content_list = page_content.split()
    for word in content_list:
        add_to_index(index,word,url)

#add_page_to_index(index,"fake.test","This is is  just a test")
#add_page_to_index(index,"another_fake.test","This is not just a test")

#Make a Hash table
def make_hashtable(nbuckets):
    hashtable = []
    for x in range(0,nbuckets):
        hashtable.append([])
    return hashtable

#Hash function
def hash_string(keyword, buckets):
    h = 0
    for c in keyword:
        h = (h + ord(c)) % buckets
    return h

#Get the bucket in the hashtable
def hashtable_get_bucket(htable, keyword):
    return htable[hash_string(keyword,len(htable))]

#Add a key,value to the bucket
def hastable_add(htable, key, value):
    hastable_get_bucket(htable, key).append([key,[value]])
    return htable

#Update the hashtable
def hashtable_update(htable,key,value):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if  entry[0] == key:
            entry[1].append(value)
            return htable
    hashtable_add(htable,key,value)
    return htable


#hashtable lookup
def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None

##Crawl the web and return the index
def crawl(seed):
    tocrawl = [seed]
    crawled = []
    index = [] 
    while tocrawl:
        url = tocrawl.pop()
        if url not in crawled:
            contents = get_page(url)
            add_page_to_index(index,url,contents)
            union(tocrawl,get_all_links(contents))
            crawled.append(url)
    return index

index = crawl('http://www.udacity.com/cs101x/index.html')
#print crawl('http://xkcd.com/353')

#print look_up(index,'<html>')

print make_hashtable(5)


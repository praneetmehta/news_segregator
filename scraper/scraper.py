import sys
sys.path.insert(0, '../pickel') #adding pickel path for module import

import newssort_loader as nl #pickel object for the news seggregator model
from bs4 import BeautifulSoup as bs
import urllib
from time import sleep
import mechanize
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from tqdm import tqdm

n = int(sys.argv[1]) #value return from node server

Client = MongoClient() #initialize mongo client
db = Client['News']
collection = db['BBC']
br = mechanize.Browser() #mechanize Browser instant initialization
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', 'Mozilla/5.0')]
br.open('http://www.news.google.com/')
# do the query
br.select_form(nr = 0)
br.form['q'] = 'bbc tech sports politics business entertainment'
data = br.submit()
soup = bs(data.read())
#for finding links on the Nth requested page from the server from google news search results
def find_links(n):
    links = []
    if(n==0):
        for a in soup.find_all('a', href=True):
            if 'www.bbc.' in a['href']:
                links.append(a['href'].split('?q=')[1].split('&sa=')[0])
        return links
    else:
        l=''
        for a in soup.find_all("a", href=True):
            if ('start='+str(n)+'0') in a['href']:
                l = a['href']
                break
        l_parsed = br.open(l)
        l_soup = bs(l_parsed)
        for a in l_soup.find_all('a', href=True):
            if 'www.bbc.' in a['href']:
                links.append(a['href'].split('?q=')[1].split('&sa=')[0])
        links = list(set(links))
        return links

def scrap_links(links):
    #stories = []
    count = 0
    for link in tqdm(links):
        count+= count
        html = urllib.urlopen(link)
        html_parsed = bs(html)

        try:
            html_head = html_parsed.h1.get_text()
            html_story = html_parsed.find("div",{"class":"story-body__inner"}).findAll("p")
            story = ' '
            news = {}
            for p in html_story:
                story+=p.text
            #stories.append({"category":nl.predict(story),"heading":html_head,"story":(' ').join(story.split(' ')[0:100])+'...'})
            news['Category'] = nl.predict(story)
            news['Heading'] = html_head
            news['Story'] = (' ').join(story.split(' ')[0:100])+'...'
            news['Link'] = link
            news['Page'] = n+1

            try:
                collection.insert_one(news)
            except DuplicateKeyError:
                db.collection.update_one({
                                           'Link': news['Link']
                                           },{
                                           '$set': {
                                                    'Category': nl.predict(story),
                                                    'Story':story
                                                    }
                                              }, upsert=False)
            sleep(1)
        except:
            sleep(1)
def main():
    links = find_links(n)
    scrap_links(links)

if __name__ == '__main__':
    main()

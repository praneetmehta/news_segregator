import sys
sys.path.insert(0, '../pickel')

import newssort_loader as nl
from bs4 import BeautifulSoup as bs
import urllib
from time import sleep
import mechanize
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from tqdm import tqdm
Client = MongoClient()
db = Client['News']
collection = db['BBC']


br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', 'Mozilla/5.0')] 
br.open('http://www.news.google.com/')   
# do the query
br.select_form(nr = 0)   
br.form['q'] = 'bbc tech sports politics business entertainment'
 # query
data = br.submit()
soup = bs(data.read())
links = []
for a in soup.find_all('a', href=True):
    if 'www.bbc.' in a['href']:
        links.append(a['href'].split('?q=')[1].split('&sa=')[0])

for i in range(2,5):
    l=''
    for a in soup.find_all("a", href=True):
        if 'start='+str(i-1)+'0' in a['href']:
            l = a['href']
            break   
    l_parsed = br.open(l)
    l_soup = bs(l_parsed)
    for a in l_soup.find_all('a', href=True):
        if 'www.bbc.' in a['href']:
            links.append(a['href'].split('?q=')[1].split('&sa=')[0])
links = list(set(links))
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
        try:
            collection.insert_one(news)
        except DuplicateKeyError:
            db.ProductData.update_one({
                                       'Link': news['Link']
                                       },{
                                       '$set': {
                                                'Category': nl.predict(story),
                                                'Story':story
                                                }
                                          }, upsert=False)
    except:
        print 'error'
    if count%10 == 0:
        sleep(1)
    else:
        sleep(1)
    

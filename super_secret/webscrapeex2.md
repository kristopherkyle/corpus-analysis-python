# Webscraping Exercise 1: Extract Relevant URLs from Wikipedia

In this exercise, the goal is to extract urls from a particular section of a Wikipedia page. This task involves examining the html structure of a page and extracting the desired links (but ONLY the desired ones).

In particular, we will try to scrape all urls to articles in the "Overviews" section on <a href="https://en.wikipedia.org/wiki/Wikipedia:Contents/Technology_and_applied_sciences" target="_blank">this Wikipedia Page</a>.

## Import relevant modules
```python
import requests
import time
from bs4 import BeautifulSoup
from corpus_toolkit import corpus_tools as ct
```

## Load and parse page
```python
wiki = requests.get("https://en.wikipedia.org/wiki/Wikipedia:Contents/Technology_and_applied_sciences")

wiki_soup = BeautifulSoup(wiki.content, 'html.parser')
```

## Grabbing all links
If we weren't looking for particular links, we could use the code below. Of course, this would include some noise, and as we see there are 1001 links on the page.

```python
wiki_urls = []
for x in wiki_soup.find_all(["a"]): #get title from page
	if x.has_attr("href") == True: #check to see if a tag has a "href" attribute
		wiki_urls.append(x["href"])

len(wiki_urls) #1001
```

## Grabbing only links that we want
There are a number of approaches we could use to filtering the desired links. In this case, we will use a couple of "switches" to start collecting urls when we hit the relevant section and then stop collecting urls when we get to the end of the section. In this case, we know that the section starts with an article with the title "Accelerating change" and ends with an article with the title "Space Transport". See code below.

```python
wiki_urls2 = []
start = False
stop = False
for x in wiki_soup.find_all(["a"]): #get title from page
	if x.has_attr("href") == True and x.has_attr("title") == True: #check to see if a tag has a "href" attribute and a "title" attribute
		#as long as start = False, no data will be collected
		if x["title"] == "Accelerating change": #when we hit this <a> tag, we will start collecting urls
			start = True
		if x["title"] == "Space transport": #when we hit this one, we will stop collecting tags
			stop = True
		if start == True: #if the start switch has been turned on, collect the url!
			wiki_urls2.append(x["href"])
		if stop == True: #break the loop if the "stop" switch has been turned on.
			break

len(wiki_urls2) #160

print(wiki_urls2[0]) #/wiki/Accelerating_change
print(wiki_urls2[-2:]) #['/wiki/Vehicle', '/wiki/Space_transport']
```

## Getting full links and scraping corpus

As we see when we looked at our list of urls, they are not complete (they are missing the beginning of the url: https://en.wikipedia.org). So, to compile our corpus, we need to do two things:
- prepend the beginning of the wikipedia url to each link in our list
- scrape the relevant information from each individual page

By looking at the source html for one of the pages, we see that most of the content on the page is within "p" tags. We may also want the headings for each section, which are within "h1", "h2", and "h3" tags. We will use BeautifulSoup to extract all text from these tags in order to build our corpus.

```python
def wiki_scraper(urllist,taglist,prelink = None):
	wiki_corpus = [] #holder for entire corpus
	for link in urllist:
		full_link = prelink + link
		wiki_page = [] #holder for page
		time.sleep(3) #pause between requests!
		print("Processing: " + full_link)
		page = requests.get(full_link) #download .html
		soup = BeautifulSoup(page.content, 'html.parser') #parse html page
		for text in soup.find_all(taglist): # text from target tags ["h1","h2","h3","p"]
			wiki_page.append(text.get_text())
		wiki_corpus.append("\n".join(wiki_page)) #combine list items into a single string and add text data to wiki_corpus list
	return(wiki_corpus)

#scrape wiki corpus
wiki_corpus = wiki_scraper(wiki_urls2, ["h1","h2","h3","p"], "https://en.wikipedia.org")
```

## Run simple frequency analysis on corpus using corpus_toolkit

Now, we can run analyses on our corpus as desired! Below, we run a simple frequency analysis.

```python
wiki_freq = ct.frequency(ct.tokenize(wiki_corpus))
print("Number of tokens in corpus: ", sum(wiki_freq.values()))
ct.head(wiki_freq) #print top frequency hits
```

```
Number of tokens in corpus:  577413
the	33357
of	21096
be	20020
and	18867
a	18068
to	14574
in	13753
that	5522
for	5435
have	4385
by	4267
or	3985
use	3884
with	3715
it	3579
on	3382
they	2849
an	2711
from	2390
which	2172

```

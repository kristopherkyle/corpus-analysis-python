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
	if x.has_attr("href") == True and x.has_attr("title") == True: #check to see if a tag has a "href" attribute

		if x["title"] == "Accelerating change":
			start = True
		if x["title"] == "Space transport":
			stop = True
		if start == True:
			wiki_urls2.append(x["href"])
		if stop == True:
			break

len(wiki_urls2) #160

print(wiki_urls2[0]) #/wiki/Accelerating_change
print(wiki_urls2[-2:]) #['/wiki/Vehicle', '/wiki/Space_transport']
```

## Next steps...
The next task is to build our corpus of files from the urls...

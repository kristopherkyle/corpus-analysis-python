# Introduction to Web Scraping with Python
(updated 2021-11-01)

Web scraping is a method of collecting corpus data from the internet. The basics are reasonably straightforward, but each web scraping project will have its challenges. This tutorial is a very simple introduction to web scraping static .html pages using the **requests** module and **BeautifulSoup** in Python 3. For more information on web scraping in Python, please see more in-depth tutorials such as [this one](https://www.dataquest.io/blog/web-scraping-python-using-beautiful-soup/) and the docs for modules such as [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) and [Selenium](https://selenium-python.readthedocs.io/).

Note that you can see the underlying .html of any web page using Google Chrome. From the toolbar, select View -> Developer -> View Source and a new page with the .html representation will open.

## Imports
This tutorial will use the following modules:
- **requests** If this isn't installed on your system, follow the [installation instructions (using pip)](https://docs.python-requests.org/en/master/user/install/#install).
- **bs4** If this isn't installed on your system, follow the [installation instructions (using pip)](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup)
- **time** This is part of the base Python distribution (it is already installed on your system)
- **corpus_toolkit** If this isn't installed on your system, follow the [installation instructions (using pip)](https://kristopherkyle.github.io/corpus_toolkit/)

```python
import requests
import time
from bs4 import BeautifulSoup
from corpus_toolkit import corpus_tools as ct
```

## Getting started: HTML
HTML is similar to XML in that it consists (primarily) of tags, tag attributes, and text. Using an html parser such as BeautifulSoup, we can search and extract particular pieces of data. Below is a (very!) simple example of an html string. Note that we could save this string in a file (e.g., sample.html), and then open it with a web browser (which would render the html).

```python
sample1 = """
<html>
<head>This is a sample header</head>
<body>
<p>This is a sample paragraph</p>
<p>This is a second paragraph</p>
<p>This is a paragraph with a link: <a href = "https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_9.html">click here!</a></p>
</body>
</html>
"""
```

## Parsing HTML
We will use BeautifulSoup to parse a static .html page.

### Extract all text
First, we will start with our sample page and extract all text.

```python
#Parse html with beautiful soup
soup1 = BeautifulSoup(sample1, 'html.parser')

#we can get all text from a page, but this usually extracts more text than we want.
text1 = soup1.text
print(text1)
```

```


This is a sample header

This is a sample paragraph
This is a second paragraph
This is a paragraph with a link: click here!


```

### Extract all text within particular tags
It is usually better practice to get text from particular tags. Below we will extract all text that is within paragraph (<p>) tags:

```python
#We can also get all text within particular tags (e.g., within "p" tags):"
list1 = []
for x in soup1.find_all('p'):
	list1.append(x.get_text())
	print(x.get_text())
```

```
This is a sample paragraph
This is a second paragraph
This is a paragraph with a link: click here!
```

### Extract other information
We can also extract information from tag attributes. One helpful application of this is to extract all URLs on a page (which are usually found in the "href" attribute of <a> tags):

```python
links1 = []
for x in soup1.find_all('a'): #look at all <a> tags
	links1.append(x["href"]) #extract all "href" attributes
	print(x["href"])
```

```
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_9.html
```

## Downloading HTML from a Web Page
We can use the **requests** module to download HTML from a web page as a string (which can be parsed with BeautiulSoup). As we can see, most html pages are more complicated than our very simple sample. Nonetheless the general format is the same.

### Download data

```python
sample2 = requests.get("https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_9.html")

print(sample2.content[:500]) #print first 500 characters of the string
```

```
b'<!DOCTYPE html>\n<html lang="en-US">\n  <head>\n    <meta charset="UTF-8">\n\n<!-- Begin Jekyll SEO tag v2.6.1 -->\n<title>Python Tutorial 9: Calculating and Outputting Text-Level Variables | Introduction to Corpus Analysis With Python 3</title>\n<meta name="generator" content="Jekyll v3.9.0" />\n<meta property="og:title" content="Python Tutorial 9: Calculating and Outputting Text-Level Variables" />\n<meta property="og:locale" content="en_US" />\n<link rel="canonical" href="https://kristopherkyle.github.'
```

## Extract information

First, we will extract all text from <p> tags:

```python
soup2 = BeautifulSoup(sample2.content, 'html.parser')

list2 = []
for x in soup2.find_all('p'):
	list2.append(x.get_text())
	print(x.get_text())
```

```
Back to Tutorial Index
(updated 11-19-2020)
In this tutorial, we will apply concepts learned in previous tutorials to create a program that reads in files (e.g., learner corpus texts), calculates a number of indices (i.e., number of words, average frequency score, lexical diversity score) for each text, and then writes the output to a tab-delimited spreadsheet file. This basic program has the building blocks for the creation of much more complex programs (like TAALED and TAALES).
We will use a frequency list derived from the Brown Corpus and will process a version of the NICT JLE learner corpus. Of course, this code could be used for a wide variety of purposes (and corpus types). Click here to download version of corpus used in this tutorial.
First, we will import the packages necessary for subsequent functions:
Then, we will import our frequency list using code we generated while completing the exercises from Python Tutorial 3:
Finally, we import our frequency list (see bottom of this tutorial for the code used to create the frequency list). The frequency list can be downloaded here.
First, we will use the safe_divide() function from Tutorial 3.
Then we will create a simple function for calculating the number of words in a text.
Next, we will create a function that will calculate the average (log-transformed) frequency value for the words in each text. This function will look up each word in a text, find the frequency of that word in a reference corpus, log-transform the frequency value (to help account for the Zipfian distribution of words in a corpus), and create an averaged score for the whole text.
Finally (for now), we will create a function that calculates a score representing the diversity of lexical items in a text. This particular index, moving average type-token ratio (MATTR) has been shown to be independent of text length (unlike many other well-known indices). See Covington et al. (2010), Kyle et al. (2020), and/or Zenker and Kyle (2020) for more details.
We will use a version of the tokenize() function from Tutorial 4 to tokenize our texts.
Now, we can create a function text_processor() that will read all files in a folder, calculate a number of lexical indices, and then outputs those to a tab-delimited file.
Below, we use our text_processor() function to calculate lexical indices in the NICT JLE learner corpus (though almost any properly-formatted corpus could be used!)
The output file generated by this code is available here.
The code used for generating the frequency list can be found below (note that the tokenize() function above is referenced here as well).
```

We can also extract all links. As we see below, there are a variety of links (some are for data downloads, some are for external pages, and others are for internal pages). To do something meaningful with the links, we would need to filter them (see next section).

```python
links2 = []
for x in soup2.find_all('a'):
	if x.has_attr("href") != True: #skip any 'a' tags that don't have an "href" attribute
		continue
	links2.append(x["href"])
	print(x["href"])
```

```
https://github.com/kristopherkyle/corpus-analysis-python
/corpus-analysis-python/py_index.html
https://www.linguisticanalysistools.org/taaled.html
https://www.linguisticanalysistools.org/taales.html
https://alaginrc.nict.go.jp/nict_jle/index_E.html
https://github.com/kristopherkyle/corpus-analysis-python/raw/master/sample_data/NICT_JLE_Cleaned.zip
/corpus-analysis-python/Python_Tutorial_3.html
https://raw.githubusercontent.com/kristopherkyle/corpus-analysis-python/master/sample_data/brown_freq_2020-11-19.txt
/corpus-analysis-python/Python_Tutorial_3.html
/corpus-analysis-python/Python_Tutorial_4.html
https://raw.githubusercontent.com/kristopherkyle/corpus-analysis-python/master/sample_data/lex_richness_JLE.txt
https://github.com/kristopherkyle/corpus-analysis-python
https://github.com/kristopherkyle
https://pages.github.com
```

## Recursively Scraping a Series of Web Pages
Once we understand the html structure of a particular website, we can often write a script that will find all relevant pages on the website and extract the desired information. Note that it is ESSENTIAL to make your script pause between html requests. Not doing this will potentially make the website crash and will likely lead to the website blocking your IP address (so you won't be able to access it again via Python). Again, you MUST use time.sleep() in your script.

To scrape our Python tutorial page, we will first gather all relevant URLs (web addresses) from the [Python Tutorials landing page](https://kristopherkyle.github.io/corpus-analysis-python/py_index.html). Then we will filter them so that they only include the pages we want to scrape. Finally, we will extract all desired data from each page.

### Get links
First we will get all links from the landing page:

```python
sample3 = requests.get("https://kristopherkyle.github.io/corpus-analysis-python/py_index.html") #get html from index page
soup3 = BeautifulSoup(sample3.content, 'html.parser') #parse html

links3 = []
for x in soup3.find_all(['a']): #we can also search other tags by adding them to the list
	if x.has_attr("href") != True: #skip any 'a' tags that don't have an "href" attribute
		continue
	links3.append(x["href"])
	print(x["href"])
```

```
https://github.com/kristopherkyle/corpus-analysis-python
/corpus-analysis-python/
/corpus-analysis-python/Python_Tutorial_1.html
/corpus-analysis-python/Python_Tutorial_2.html
/corpus-analysis-python/Python_Tutorial_3.html
/corpus-analysis-python/Python_Tutorial_4.html
/corpus-analysis-python/Python_Tutorial_5.html
/corpus-analysis-python/Python_Tutorial_6.html
/corpus-analysis-python/Python_Tutorial_7.html
/corpus-analysis-python/Python_Tutorial_8.html
/corpus-analysis-python/Python_Tutorial_9.html
/corpus-analysis-python/PySupp1_lemmatization.html
/corpus-analysis-python/PySupp2_Concord.html
https://github.com/kristopherkyle/corpus-analysis-python
https://github.com/kristopherkyle
https://pages.github.com
```

As we can see, there are links to pages other than the main tutorials (which include "Tutorial") in the URL. We will include an `if` statement to include only the main tutorial pages.

```python
#we only want the tutorials, so we will use an "if" statement to filter our links
links3 = []
for x in soup3.find_all(['a']):
	if x.has_attr("href") != True: #skip any 'a' tags that don't have an "href" attribute
		continue
	if "Tutorial" in x["href"]: #only include links with "Tutorial in URL"
		links3.append(x["href"])
		print(x["href"])

```

```
/corpus-analysis-python/Python_Tutorial_1.html
/corpus-analysis-python/Python_Tutorial_2.html
/corpus-analysis-python/Python_Tutorial_3.html
/corpus-analysis-python/Python_Tutorial_4.html
/corpus-analysis-python/Python_Tutorial_5.html
/corpus-analysis-python/Python_Tutorial_6.html
/corpus-analysis-python/Python_Tutorial_7.html
/corpus-analysis-python/Python_Tutorial_8.html
/corpus-analysis-python/Python_Tutorial_9.html
```

Finally, we see that the URLs are not complete, so we will add the missing URL information:

```python
links3 = []
#finally, we can see that we don't have a full URL, so we need to add the beginning of the URL to our links
web_address = "https://kristopherkyle.github.io"
links3 = []
for x in soup3.find_all(['a']):
	if x.has_attr("href") != True: #skip any 'a' tags that don't have an "href" attribute
		continue
	if "Tutorial" in x["href"]:
		links3.append(web_address + x["href"])
		print(web_address + x["href"])
```

```
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_1.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_2.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_3.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_4.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_5.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_6.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_7.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_8.html
https://kristopherkyle.github.io/corpus-analysis-python/Python_Tutorial_9.html
```

### Extract text from each link
Now that we have the appropriate links, we can extract the appropriate text data from each page and include it in a corpus.

```python
py_corpus = []
for link in links3:
	full_text = [] #holder for all texts on a page
	time.sleep(3) #pause for three seconds in-between requests
	print("Processing: " + link)
	page = requests.get(link) #download .html
	soup = BeautifulSoup(page.content, 'html.parser') #parse html page
	for text in soup.find_all(['p']):
		full_text.append(text.get_text())
	py_corpus.append("\n".join(full_text)) #combine list items into a single string and add text data to corpus1 list

print(py_corpus[0][:500]) #print sample of the first corpus document
```

```
Back to Tutorial Index
Updated 9-21-2020
In the programming tradition, we must begin with the following program:
Python has three basic types of values:
Strings are sequences of characters that are interpreted as text
Strings are defined using quotation marks (“ or ‘)
Integers are whole numbers (i.e., have no decimal places)
Integers can be added, subtracted, multiplied, and divided.
Floats are numbers that have decimal places
When integers are divided, they are converted to floats
Defining vari
```

## Corpus Analyses with our Scraped Corpus
Now that we have a (very small) corpus of scraped documents, we can conduct corpus analyses!

```python
#tokenize and get frequency list:
py_freq = ct.frequency(ct.tokenize(py_corpus))
ct.head(py_freq, hits = 10)
```

```
the	397
we	295
a	278
be	206
to	199
of	199
in	169
will	152
and	150
function	137
```

## Final notes
There is no "one-size-fits-all" approach to web scraping. For example, your desired content will not always be in <p> tags, and web pages will often have links that you don't want to use. The key to successful scraping is understanding the structure of a particular website and (sometimes creatively) using the structure to extract the desired information (and ignore the rest).

Good luck!

# Python Tutorial 4: Tokenization, Lemmatization, and Frequency Lists
[Back to Tutorial Index](py_index.md)

(updated 10-2-2020)

In this tutorial, we will work on basic corpus analysis functions. 	

We will work on completing smaller tasks, including:
- tokenization
- lemmatization
- frequency calculation

And then combine these tasks in a larger function that will read in a corpus and output a frequency dictionary. While there are many ways that we can use Python to accomplish this end goal, we will focus on writing simple scripts that are scalable (i.e., can be used with corpora of various sizes) and easily extended/revised for your own purposes.

### Tokenization
We will read in a corpus file as a string. Our first step will be to convert the string of characters into a list of strings (words) that we can count and otherwise manipulate. We will also want to ensure that our characters are in the desired format (e.g., lower case, upper case, or a mix of the two) and that unwanted characters (such as punctuation marks) are separated from words (and/or removed).

For this function, we will use the **_.split()_** method (which we have discussed in previous tutorials).

For cleaning, we will use the **_.replace()_** method, which allows use to replace any string of characters with another string of characters.

In the example below, we will replace all periods "." with a period and a space " .", which will separate periods from words, but will still retain them in our corpus.
```python
#In this example, we will replace any periods with nothing (i.e., we will delete any periods)
text = "This is a sample string."
clean_text = text.replace("."," .")
print(clean_text)
```
```
> This is a sample string .
```
Note that we could also use [regular expressions](https://docs.python.org/3/library/re.html) to delete/replace characters. While regular expressions can be very powerful, they are also more complicated, so we will hold off on discussing them (for now).

Below, we use the **_.replace()_** and **_.split()_** methods to write a function called **_tokenize()_**, which will take a string as an argument and output a tokenized list.
```python
def tokenize(input_string):
	tokenized = [] #empty list that will be returned

	#this is a sample (but incomplete!) list of punctuation characters
	punct_list = [".", "?","!",",","'"]

	#this is a sample (but potentially incomplete) list of items to replace with spaces
	replace_list = ["\n","\t"]

	#This is a sample (but potentially incomplete) list if items to ignore
	ignore_list = [""]

	#iterate through the punctuation list and replace each item with a space + the item
	for x in punct_list:
		input_string = input_string.replace(x," " + x)

	#iterate through the replace list and replace it with a space
	for x in replace_list:
		input_string = input_string.replace(x," ")

	#our examples will be in English, so for now we will lower them
	#this is, of course optional
	input_string = input_string.lower()

	#then we split the string into a list
	input_list = input_string.split(" ")

	#finally, we ignore unwanted items
	for x in input_list:
		if x not in ignore_list: #if item is not in the ignore list
			tokenized.append(x) #add it to the list "tokenized"

	#Then, we return the list
	return(tokenized)
```
Now, we can try out our new function:

```python
s1 = "This is a sample sentence. This is one too! Is this?"
l1 = tokenize(s1)
print(l1)
```
```
> ['this', 'is', 'a', 'sample', 'sentence', '.', 'this', 'is', 'one', 'too', '!', 'is', 'this', '?']
```

### Lemmatization

There are many methods of lemmatizing. Here, we will use a very simple (but imperfect) dictionary-based method, which is increasingly referred to as "flemmatization" (see, e.g., Kyle, 2020). Note that with the methods below, we can also familize a text (as is commonly done in the Paul Nation tradition of vocabulary analysis; see Nation, 2006 for more details on word families).

In order to lemmatize our corpus, we need to complete two tasks. First, we need to load a lemma dictionary. Then, we will use that dictionary to convert a tokenized corpus into a lemmatized version.

For this tutorial, we will load a lemma dictionary that I already generated from the list provided by [Laurence Anthony](https://www.laurenceanthony.net/resources/wordlists/antbnc_lemmas_ver_003.zip). For sake of simplicity and brevity, I am not going to go over generating the dictionary from a text file, but if you are interested, [the code is available here.](PySupp1_lemmatization.md)

Instead, we will load the lemma dictionary directly, using the [**_pickle()_**](https://docs.python.org/3/library/pickle.html) module. Make sure that ["ant_lemmas.pickle"](https://github.com/kristopherkyle/corpus-analysis-python/raw/master/sample_data/ant_lemmas.pickle) is in your working directory, then run the following code to load it:
```python
import pickle #load pickle module
lemma_dict = pickle.load("ant_lemmas.pickle","rb") #open pickled dictionary and assign it to lemma_dict
```
The lemma dictionary includes word form : lemma pairs, as is demonstrated below:
```python
print(lemma_dict["is"])
print(lemma_dict["ran"])
```
```
> be
> run
```

Now that we have a lemma dictionary, we can easily turn a tokenized text into a lemmatized text.

The function **_lemmatize()_** below takes two arguments (a list of words and a lemma_dictionary) and returns a list of lemmas.
1. **_tokenized_** is a tokenized list of words
2. **_lemma_d_** is a lemma dictionary that consists of {"word" : "lemma"} pairs

```python
def lemmatize(tokenized,lemma_d): #takes a tokenized list words and a lemma dictionary as arguments
	lemmatized = [] #holder for lemma list

	for word in tokenized: #iterate through words in text
		if word in lemma_d: #if word is in lemma dictionary
			lemmatized.append(lemma_d[word]) #add the lemma for to lemma_text
		else:
			lemmatized.append(word) #otherwise, add the raw word to the lemma_text

	return(lemmatized) #return lemmatized corpus
```
Now, we can create a lemmatized version of our sample text:
```python
lemma1 = lemmatize(l1, lemma_dict)
print(lemma1)
```
```
> ['this', 'be', 'a', 'sample', 'sentence', '.', 'this', 'be', 'one', 'too', '!', 'be', 'this', '?']
```

### Frequency calculation
To calculate frequency, we will create a dictionary that stores each word in our corpus and the number of times that the word is encountered. The sample function below **_freq_simple()_** takes one argument (a list of words) and returns a frequency dictionary.

```python
def freq_simple(tok_list):
	#first we define an empty dictionary
	freq = {}

	#then we iterate through our list
	for x in tok_list:
		#the first time we see a particular word we create a key:value pair
		if x not in freq:
			freq[x] = 1
		#when we see a word subsequent times, we add (+=) one to the frequency count
		else:
			freq[x] += 1
	#finally, we return the frequency dictionary
	return(freq)
```
Now, we can use our function to create a frequency dictionary for the sample text we tokenized and lemmatized above.
```python
freq1 = freq_simple(lemma1)
print(freq1)
```
```
> {'this': 3, 'be': 3, 'a': 1, 'sample': 1, 'sentence': 1, '.': 1, 'one': 1, 'too': 1, '!': 1, '?': 1}
```
As we can see above, "this" and "be" each occurred three times, while all other words only occurred once.

### Putting it all together: Creating a corpus frequency list
In this section, we will create a lemmatized frequency list for the [Brown corpus](http://www.helsinki.fi/varieng/CoRD/corpora/BROWN/). To do so, we will write a function that:
- Finds all relevant files in a folder (i.e., all of our corpus documents)
- Reads each file
- Tokenizes each file
- Lemmatizes each file
- Calculates frequency figures for the entire corpus_list
- Returns a frequency dictionary

While this may seem like a lot to do, we have already created most of the building blocks. We will use our **_tokenize()_** and **_lemmatize()_** functions. We will also integrate pieces of the code of our **_freq_simple()_** function.

In addition, will use a new module, **_glob()_** which creates lists of files that match certain criteria.

```python
import glob
def corpus_freq(dir_name,lemma_d):
	freq = {} #create an empty dictionary to store the word : frequency pairs

	#create a list that includes all files in the dir_name folder that end in ".txt"
	filenames = glob.glob(dir_name + "/*.txt")

	#iterate through each file:
	for filename in filenames:
		#open the file as a string
		text = open(filename, errors = "ignore").read()
		#tokenize text using our tokenize() function
		tokenized = tokenize(text)
		#lemmatize text using the lemmatize() function
		lemmatized = lemmatize(tokenized,lemma_d)

		#iterate through the lemmatized text and add words to the frequency dictionary
		for x in lemmatized:
			#the first time we see a particular word we create a key:value pair
			if x not in freq:
				freq[x] = 1
			#when we see a word subsequent times, we add (+=) one to the frequency count
			else:
				freq[x] += 1

	return(freq)
```
Now, lets try out our function. To do so, download [brown_corpus.zip](https://github.com/kristopherkyle/corpus-analysis-python/raw/master/sample_data/brown_corpus.zip) and put the folder in your working directory. For Windows users, you may have two folders named "brown_corpus" (one within the other). If so, make sure to take the folder that has 15 text files in it and put it directly in your working directory (i.e., not inside another folder). Then, we can run the following code:

```python
brown_freq = corpus_freq("brown_corpus",lemma_dict)
print(brown_freq["be"])
print(brown_freq["climb"])
print(brown_freq["awesome"])
```
```
> 43817
> 68
> 4
```

Although frequency dictionaries can be very useful in a variety of applications, we may also want to look at a sorted version of the list, and we may also want to write the frequency list to a file. We will complete these final (for now) steps below.

```python
import operator #this module will help us convert our dictionary into an ordered structure
#we won't take the time to completely break it down, but the following code sorts our dictionary by value (i.e., by frequency) in descending order
sorted_brown = sorted(brown_freq.items(),key=operator.itemgetter(1),reverse = True)

#print the first 20 items in our list
for x in sorted_brown[:20]:
	print(x[0],"\t",x[1]) #print the word, a tab, and then the frequency
```
```
> the      69971
,        58334
.        54328
be       43817
of       36412
a        30641
and      28853
to       26158
in       21341
he       19422
'        18674
it       13043
have     12437
that     10787
for      9491
``       8837
i        8474
they     8264
with     7289
on       6741
```

### Writing our sorted list to a file
We will write a simple tab-delimited text below.

```python
def freq_writer(freq_list,filename):
	outf = open(filename, "w")
	outf.write("word\tfrequency") #write header

	for x in freq_list:
		outf.write("\n" + x[0] + "\t" + str(x[1])) #newline character + word + tab + string version of Frequency
	outf.flush() #flush buffer
	outf.close() #close file

#this will write sorted_brown to a file named "brown_freq.txt" in your working directory
freq_writer(sorted_brown,"brown_freq.txt")
```
As you will see as you look at the frequency list, there may be some items that we want to ignore (e.g., commas, periods, and other punctuation), but otherwise our scripts worked as intended!

## Exercises
(to be added)

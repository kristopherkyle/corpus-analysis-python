# Python Tutorial 4: Corpus Loading, Tokenizing, Lemmatizing, and N-grams
[Back to Tutorial Index](py_index.md)

In this tutorial, we will work on basic corpus analysis functions. In many cases, I will provide a simple (but workable) example first, followed by a more robust method.

### Corpus Loading

We will begin by loading our corpus into the computers memory. For large corpora, we will want to only read one file into our computers' memory at once. However, in these examples we will simplify things by keeping the whole corpus in memory (though we can change this later).

First, we will import the glob package, will allow us to find all files that meet certain criteria (e.g., all .txt files in a particular folder).

```python
import glob
```

Then, we will create a function **_load_corpus()_** that will take three arguments:
1. **_dirname_** is a string. This should be the folder your corpus files are in (e.g., "sample_corpus")
2. **_ending_** is a string. This is the ending of your filename. By default, this is '.txt'.
3. **_lower_** is a Boolean value (i.e., True or False). This tells the program whether to change all words in your corpus to lower case. By default, this is true.

The function will return a list of strings (where each list item represents a corpus document).

```python
def load_corpus(dir_name, ending = '.txt', lower = True): #this function takes a directory/folder name as an argument, and returns a list of strings (each string is a document)
	master_corpus = [] #empty list for storing the corpus documents
	filenames = glob.glob(dir_name + "/*" + ending) #make a list of all ".txt" files in the directory
	for filename in filenames: #iterate through the list of filenames
		if lower == True:
			master_corpus.append(open(filename).read().lower()) #open each file, lower it and add strings to list
		else:
			master_corpus.append(open(filename).read())#open each file, (but don't lower it) and add strings to list

	return(master_corpus) #output list of strings (i.e., the corpus)

```

The example below presumes that you have some text files (with the ending '.txt') in a folder entitled "corpus_documents". It also presumes that this folder is in the same folder as your Python script (and that you have set your working directory :)).

```python
corpus_lower = load_corpus("corpus_documents") #load the corpus into memory with the default settings
print(corpus_lower[0]) #print the first document in the corpus
```

If we do not want all of our corpus characters to be in lower case, we can use "lower = False"

```python
corpus_sample = load_corpus("corpus_documents", lower = False) #load the corpus into memory with the default settings
print(corpus_sample[0]) #print the first document in the corpus
```

### Tokenizing
Next, we need to clean and tokenize our corpus so we can start counting words.

For cleaning, we will use the **_.replace()_** method, which allows use to replace any string of characters with another string of characters.

```python
#In this example, we will replace "silly" with "sample"
text1 = "This is a silly string."
text2 = text1.replace("silly","sample")
```

```
> This is a sample string.
```
We can also effectively delete characters by replacing them with nothing (using "").
```python
#In this example, we will replace any periods with nothing (i.e., we will delete any periods)
text = "This is a sample string."
clean_text = text.replace(".","")
print(clean_text)
```
```
> This is a sample string
```

In effect, a tokenizer should do (at least) two things. First, it should make any desired modifications to the corpus files (e.g., remove punctuation). Second, it should separate the files into individual word units.

The function **_tokenize()_** below will do two types of replacement (deleting strings such as punctuation marks and replacing newline characters and other spaces with single spaces) based on lists we will provide. It will then convert each file from a string to a list of word units (by splitting on spaces).

**_tokenize()_** takes four arguments:
1. **_corpus_list_** is a list of strings (i.e., corpus documents)
2. **_remove_list_** is a list of items to remove (in this case, punctuation)
3. **_space_list_** is a list of white space items to replace with a single space (e.g., tabs and newline characters)
4. **_split_token_** is the character used to split the string into word units. By default, this is a space.

The function will return a list of lists (corpus documents) of lists (word units).

```python
default_punct_list = [",",".","?","'",'"',"!",":",";","(",")","[","]","''","``","--"] #we can add more items to this if needed
default_space_list = ["\n","\t","    ","   ","  "]

def tokenize(corpus_list, remove_list = default_punct_list, space_list = default_space_list, split_token = " "):
	master_corpus = [] #holder list for entire corpus

	for text in corpus_list: #iterate through each string in the corpus_list
		for item in remove_list:
			text = text.replace(item,"") #replace each item in list with "" (i.e., nothing)
		for item in space_list:
			text = text.replace(item," ")

		#then we will tokenize the document and add it to the corpus
		tokenized = text.split(split_token) #split string into list using the split token (by default this is a space " ")

		master_corpus.append(tokenized) #add tokenized text to the master_corpus list

	return(master_corpus)

```

The example below presumes that you have a variable "corpus_lower" that is a list of strings (i.e., corpus documents)

```python
tokenized_corpus = tokenize(corpus_lower) #tokenize corpus
print(tokenized_corpus[0]) #print first document
print(tokenized_corpus[0][0]) #print first word in first document
```

### Lemmatizing

There are many methods of lemmatizing. Here, we will use a very simple (but imperfect) dictionary-based method, which is increasingly referred to as "flemmatization". Note that with the methods below, we can also familize a text (as is commonly done in the Paul Nation tradition of vocabulary analysis; see Nation, 2006 for more details on word families).

In order to lemmatize our corpus, we need to complete two tasks. First, we need to load a lemma dictionary. Then, we will use that dictionary to convert a tokenized corpus into a lemmatized version.

In the examples below, we will use a lemma list from [Laurence Anthony's AntConc webpage](https://www.laurenceanthony.net/software/antconc/), though any lemma (or family) list with the same format can be used.

The function **_load_lemma_** takes a single argument and returns a dictionary consisting of {"word" : "lemma"} pairs.
1. **_lemma_file_** is a string. It should be the name of your lemma list (don't forget place this file in the same folder as your Python script and set your working directory!)

```python
def load_lemma(lemma_file): #this is how we load a lemma_list
	lemma_dict = {} #empty dictionary for {token : lemma} key : value pairs
	lemma_list = open(lemma_file).read() #open lemma_list
	lemma_list = lemma_list.replace("\t->","") #replace marker, if it exists
	lemma_list = lemma_list.split("\n") #split on newline characters
	for line in lemma_list: #iterate through each line
		tokens = line.split("\t") #split each line into tokens
		if len(tokens) <= 2: #if there are only two items in the token list, skip the item (this fixed some problems with the antconc list)
			continue
		lemma = tokens[0] #the lemma is the first item on the list
		for token in tokens[1:]: #iterate through every token, starting with the second one
			if token in lemma_dict:#if the token has already been assigned a lemma - this solved some problems in the antconc list
				continue
			else:
				lemma_dict[token] = lemma #make the key the word, and the lemma the value

	return(lemma_dict)
```

The example below uses [Laurence Anthony's lemma list](https://www.laurenceanthony.net/resources/wordlists/antbnc_lemmas_ver_003.zip), which includes lemmas for all words that occur at least twice in the BNC.

```python
lemma_dict = load_lemma("antbnc_lemmas_ver_003.txt")
```

Now that we have a lemma dictionary, we can easily turn a tokenized text into a lemmatized text.

The function **_lemmatize()_** below takes two arguments and returns a list of lists (corpus documents) of lists (lemmas).
1. **_tokenized_corpus_** is a tokenized corpus (list of lists of lists)
2. **_lemma_** is a lemma dictionary that consists of {"word" : "lemma"} pairs

```python
def lemmatize(tokenized_corpus,lemma): #takes a list of lists (a tokenized corpus) and a lemma dictionary as arguments
	master_corpus = [] #holder for lemma corpus
	for text in tokenized_corpus: #iterate through corpus documents
		lemma_text = [] #holder for lemma text

		for word in text: #iterate through words in text
			if word in lemma: #if word is in lemma dictionary
				lemma_text.append(lemma[word]) #add the lemma for to lemma_text
			else:
				lemma_text.append(word) #otherwise, add the raw word to the lemma_text

		master_corpus.append(lemma_text) #add lemma version of the text to the master corpus

	return(master_corpus) #return lemmatized corpus
```
Now, we can create a lemmatized version of our corpus:
```python
lemmatized_corpus = lemmatize(tokenized_corpus, lemma = lemma_dict)
print(lemmatized_corpus[0]) #print first document in corpus
print(lemmatized_corpus[0][0]) #print first lemma in corpus)
```

### N-grams
We can also easily create n-gram versions of our tokenized texts.

The function **_ngrammer()_** below takes two arguments and returns a list of lists (corpus documents) of lists (n-grams).
1. **_tokenized_corpus_** is a tokenized (or lemmatized) corpus (list of lists of lists)
2. **_number_** is the number of items (words) to include in each n-gram

```python
def ngrammer(tokenized_corpus,number):
	master_ngram_list = [] #list for entire corpus

	for tokenized in tokenized_corpus:
		ngram_list = [] #empty list for ngrams
		last_index = len(tokenized) - 1 #this will let us know what the last index number is
		for i , token in enumerate(tokenized): #enumerate allows us to get the index number for each iteration (this is i) and the item
			if i + number > last_index: #if the next index doesn't exist (because it is larger than the last index)
				continue
			else:
				ngram = tokenized[i:i+number] #the ngram will start at the current word, and continue until the nth word
				ngram_string = "_".join(ngram) #turn list of words into an n-gram string
				ngram_list.append(ngram_string) #add string to ngram_list

		master_ngram_list.append(ngram_list) #add ngram_list to master list

	return(master_ngram_list)
```

```python
corpus_bigram = ngrammer(tokenized_corpus,2)
print(corpus_bigram[0])
```
```python
corpus_trigram = ngrammer(tokenized_corpus,3)
print(corpus_bigram[0])
```

# Python Tutorial 7: Keyness
[Back to Tutorial Index](py_index.md)

(updated 10-20-2020)

In this tutorial we will create a function that identifies items that occur more frequently in on corpus as compared to another (i.e., "key" items). To this end, we will reuse and revise some functions from previous tutorials. We will also explore a new way to represent texts (via n-grams).

## Getting started
First, we will load the head() function from [Python Tutorial 6](Python_Tutorial_6.md). Please see Python Tutorial 6 for more details on this function. We will be using it to preview the various lists we will generate in this tutorial.

```python
import operator
def head(stat_dict,hits = 20,hsort = True,output = False,filename = None, sep = "\t"):
	#first, create sorted list. Presumes that operator has been imported
	sorted_list = sorted(stat_dict.items(),key=operator.itemgetter(1),reverse = hsort)[:hits]

	if output == False and filename == None: #if we aren't writing a file or returning a list
		for x in sorted_list: #iterate through the output
			print(x[0] + "\t" + str(x[1])) #print the sorted list in a nice format

	elif filename is not None: #if a filename was provided
		outf = open(filename,"w") #create a blank file in the working directory using the filename
		outf.write("item\tstatistic") #write header
		for x in sorted_list: #iterate through list
			outf.write("\n" + x[0] + sep + str(x[1])) #write each line to a file using the separator
		outf.flush() #flush the file buffer
		outf.close() #close the file

	if output == True: #if output is true
		return(sorted_list) #return the sorted list
```

## Tokenization and n-grams
It is often interesting (and important) to examine linguistic units beyond single words. This is particularly true for keyness analysis. Below, we adapt our tokenize() function from [previous tutorials](Python_Tutorial_6.md) to output items of _n_ words in length. We start by defining a new function **_ngrammer()_** that takes a tokenized list as an argument and outputs a list of n-grams.

### N-grams
**_ngrammer()_** takes three arguments:
- **_token_list_** a tokenized list of words
- **_gram_size_** number of words to include in n-gram
- **_separator_** character (or characters) used to join the n-grams. Be default this is a space (" ").

```python
def ngrammer(token_list, gram_size, separator = " "):
	ngrammed = [] #empty list for n-grams

	for idx, x in enumerate(token_list): #iterate through the token list using enumerate()

		ngram = token_list[idx:idx+gram_size] #get current word token_list plus words n-words after (this is a list)

		if len(ngram) == gram_size: #don't include shorter ngrams that we would get at the end of a text
			ngrammed.append(separator.join(ngram)) # join the list of ngram items using the separator (by default this is a space), add to ngrammed list

	return(ngrammed) #return list of ngrams
```

Now, we will test our function using a sample tokenized list:

```python
sampl = ["this", "is", "an", "awesome", "sentence", "about", "pizza"]
bigram_sampl = ngrammer(sampl,2) #create bigram version of tokenized text
print(bigram_sampl)
```
```
> ['this is', 'is an', 'an awesome', 'awesome sentence', 'sentence about', 'about pizza']
```

```python
trigram_sampl = ngrammer(sampl,3)
print(trigram_sampl)
```
```
['this is an', 'is an awesome', 'an awesome sentence', 'awesome sentence about', 'sentence about pizza']
```

### Revising tokenize() function to work with n-grams
Now, we will revise our tokenize() function to work with n-grams. We will only need to add a few lines at the end of our [previous version](Python_Tutorial_6.md) and add the arguments needed for the **_ngrammer()_** function.

The updated version of the **_tokenize()_** function takes three arguments and outputs a tokenized text (a list):
- **_input_string_** a raw string consisting of language data
- **_gram_size_** number of words to include in n-gram. By default this is one (i.e., the default is to tokenize "normally")
- **_separator_** character (or characters) used to join the n-grams (if gram_size > 1). Be default this is a space (" ").

```python
def tokenize(input_string,gram_size=1, separator = " "): #input_string = text string

	tokenized = [] #empty list that will be returned

	#these are the punctuation marks in the Brown corpus + '"'
	punct_list = ['-',',','.',"'",'&','`','?','!',';',':','(',')','$','/','%','*','+','[',']','{','}','"']

	#this is a sample (but potentially incomplete) list of items to replace with spaces
	replace_list = ["\n","\t"]

	#This is a sample (but potentially incomplete) list if items to ignore
	ignore_list = [""]

	#iterate through the punctuation list and delete each item
	for x in punct_list:
		input_string = input_string.replace(x, "") #instead of adding a space before punctuation marks, we will delete them (by replacing with nothing)

	#iterate through the replace list and replace it with a space
	for x in replace_list:
		input_string = input_string.replace(x," ")

	#our examples will be in English, so for now we will lower them
	#this is, of course optional
	input_string = input_string.lower()

	#then we split the string into a list
	input_list = input_string.split(" ")

	for x in input_list:
		if x not in ignore_list: #if item is not in the ignore list
			tokenized.append(x) #add it to the list "tokenized"

	if gram_size == 1: #if we are looking at single words, simply return tokenized
		return(tokenized)

	else: #otherwise, return n-gram text, using the ngrammer() function
		return(ngrammer(tokenized,gram_size,separator))
```
Now we can use our **_tokenize()_** function to create various versions of a texts:

Single word tokenized:
```python
samps = "This is an awesome sentence about pizza."
tok_samps = tokenize(samps) #tokenize with default gram_size (1)
print(tok_samps)
```
```
> ['this', 'is', 'an', 'awesome', 'sentence', 'about', 'pizza']
```
Bigram tokenized:
```python
bigram_samps = tokenize(samps,2)
print(bigram_samps)
```
```
>['this is', 'is an', 'an awesome', 'awesome sentence', 'sentence about', 'about pizza']
```
Trigram tokenized:
```python
trigram_samps = tokenize(samps,3)
print(trigram_samps)
```
```
> ['this is an', 'is an awesome', 'an awesome sentence', 'awesome sentence about', 'sentence about pizza']
```

## Calculating corpus frequency
To calculate keyness, we will need to first create frequency dictionaries for each of our comparison corpora. To do so, we will revise the **_corpus_freq()_** function from [Python Tutorial 4](Python_Tutorial_6.md). In this case, we will add the arguments needed to use our revised version of the **_tokenize()_** function and change one line slightly to accommodate these arguments.

The **_corpus_freq()_** function takes three arguments:
- **_dir_name_** name of folder that holds our corpus files (don't forget to set your working directory!)
- **_gram_size_** number of words to include in n-gram. By default this is one (i.e., the default is to tokenize "normally")
- **_separator_** character (or characters) used to join the n-grams (if gram_size > 1). Be default this is a space (" ").

```python
import glob
def corpus_freq(dir_name,gram_size = 1,separator = " "):
	freq = {} #create an empty dictionary to store the word : frequency pairs

	#create a list that includes all files in the dir_name folder that end in ".txt"
	filenames = glob.glob(dir_name + "/*.txt")

	#iterate through each file:
	for filename in filenames:
		#open the file as a string
		text = open(filename, errors = "ignore").read()
		#tokenize text using our tokenize() function
		tokenized = tokenize(text,gram_size) #use tokenizer indicated in function argument (e.g., "tokenize()" or "ngramizer()")

		#iterate through the tokenized text and add words to the frequency dictionary
		for x in tokenized:
			#the first time we see a particular word we create a key:value pair
			if x not in freq:
				freq[x] = 1
			#when we see a word subsequent times, we add (+=) one to the frequency count
			else:
				freq[x] += 1

	return(freq) #return frequency dictionary
```
Now we can generate various frequency lists. Below we will test out our function using the Brown Corpus.

First, we will use the default settings to get a word frequency list:
```python
brown_freq =  corpus_freq("brown_corpus")
head(brown_freq,10)
```
```
> the     69971
of      36412
and     28853
to      26158
a       23308
in      21341
that    10594
is      10109
was     9815
he      9548
```

Then bigrams:
```python
brown_bi_freq = corpus_freq("brown_corpus",2)
head(brown_bi_freq,10)
```
```
> of the  9739
in the  6055
to the  3500
on the  2482
and the 2256
for the 1858
to be   1718
at the  1660
with the        1543
of a    1480
```
Then trigrams:
```python
brown_tri_freq = corpus_freq("brown_corpus",3)
head(brown_tri_freq,10)
```
```
> one of the      404
the united states       340
as well as      238
some of the     179
out of the      174
the fact that   167
the end of      149
part of the     144
it was a        143
there was a     142
```
And beyond...:
```python
brown_quad_freq = corpus_freq("brown_corpus",4)
head(brown_quad_freq,10)
```
```
> of the united states    111
at the same time        87
the end of the  77
in the united states    70
at the end of   63
the rest of the 58
on the other hand       58
one of the most 58
on the basis of 56
as well as the  48
```

## Calculating keyness
A number of statistical procedures have been suggested for calculating keyness. Our function will calculate three keyness statistics described in Gabrielatos (2018), though our function could be easily extended to include more! In our calculation of the three keyness statistics, we will ignore items that only occur in one of the corpora. However, the function will report these items (and their normalized frequency) in separate dictionaries (see below).

The **_keyness()_** function takes two arguments:
- **_freq_dict1_** frequency dictionary for target corpus (raw frequencies)
- **_freq_dict2_** frequency dictionary for comparison corpus (raw frequencies)

and returns a dictionary of dictionaries:
- **_"log-ratio"_** log ratio (see Gabrielatos (2018); Hardie (2014))
- **_"%diff"_** percent difference (see Gabrielatos (2018); Gabrielatos and Marchi (2011))
- **_"odds-ratio"_** odds ratio (see Gabrielatos (2018); Everitt (2002))
- **_"c1_only"_** items that only occur in the target corpus (corpus 1)
- **_"c2_only"_** items that only occur in the comparison corpus (corpus 2)

```python
import math
def keyness(freq_dict1,freq_dict2): #this assumes that raw frequencies were used. effect options = "log-ratio", "%diff", "odds-ratio"
	keyness_dict = {"log-ratio": {},"%diff" : {},"odds-ratio" : {}, "c1_only" : {}, "c2_only":{}}

	#first, we need to determine the size of our corpora:
	size1 = sum(freq_dict1.values()) #calculate corpus size by adding all of the values in the frequency dictionary
	size2 = sum(freq_dict2.values()) #calculate corpus size by adding all of the values in the frequency dictionary

	#How to calculate three measures of keyness:
	def log_ratio(freq1,size1,freq2,size2):  #see Gabrielatos (2018); Hardie (2014)
		freq1_norm = freq1/size1 * 1000000 #norm per million words
		freq2_norm = freq2/size2 * 1000000 #norm per million words
		index = math.log2(freq1_norm/freq2_norm) #calculate log ratio
		return(index)

	def perc_diff(freq1,size1,freq2,size2): #see Gabrielatos (2018); Gabrielatos and Marchi (2011)
		freq1_norm = freq1/size1 * 1000000 #norm per million words
		freq2_norm = freq2/size2 * 1000000 #norm per million words
		index = ((freq1_norm-freq2_norm) * 100)/freq2_norm #calculate perc_diff
		return(index)

	def odds_ratio(freq1,size1,freq2,size2): #see Gabrielatos (2018); Everitt (2002)
		index = (freq1/(size1-freq1))/(freq2/(size2-freq2))
		return(index)


	#make a list that combines the keys from each frequency dictionary:
	all_words = set(list(freq_dict1.keys()) + list(freq_dict2.keys())) #set() creates a set object that includes only unique items

	#if our items only occur in one corpus, we will add them to our "c1_only" or "c2_only" dictionaries, and then ignore them
	for item in all_words:
		if item not in freq_dict1:
			keyness_dict["c2_only"][item] = freq_dict2[item]/size2 * 1000000 #add normalized frequency (per million words) to c2_only dictionary
			continue #move to next item in the list
		if item not in freq_dict2:
			keyness_dict["c1_only"][item] = freq_dict1[item]/size1 * 1000000 #add normalized frequency (per million words) to c1_only dictionary
			continue #move to next item on the list

		keyness_dict["log-ratio"][item] = log_ratio(freq_dict1[item],size1,freq_dict2[item],size2) #calculate keyness using log-ratio

		keyness_dict["%diff"][item] = perc_diff(freq_dict1[item],size1,freq_dict2[item],size2) #calculate keyness using %diff

		keyness_dict["odds-ratio"][item] = odds_ratio(freq_dict1[item],size1,freq_dict2[item],size2) #calculate keyness using odds-ratio

	return(keyness_dict) #return dictionary of dictionaries
```
Now we will test our keyness function using two subsets of the Brown corpus. The first will be texts from newspapers (reportage, editorials, and reviews). The second will be texts that represent various types of fiction (general, mystery, science, adventure, and romance). In practice, we would want to use larger corpora (if possible), but for our purposes these two subcorpora will be adequate.

To start, download the two corpora: [brown_press.zip](https://github.com/kristopherkyle/corpus-analysis-python/raw/master/sample_data/brown_press.zip) and [brown_fiction.zip](https://github.com/kristopherkyle/corpus-analysis-python/raw/master/sample_data/brown_fiction.zip). Then expand the corpora and place them in your working directory.

After the two corpora have been placed in your working directory, we can frequency dictionaries for each

```python
brown_news_freq = corpus_freq("brown_press")
head(brown_news_freq,10)
```
```
> the     12711
of      6191
and     4701
to      4453
a       4263
in      3837
is      2016
for     1810
that    1792
s       1309
```

```python
brown_fic_freq = corpus_freq("brown_fiction")
head(brown_fic_freq,10)
```
```
> the     14100
and     6957
to      5947
a       5590
of      5194
he      5111
was     4153
in      3652
i       3356
it      2955
```

Then, we can use the **_keyness()_** function to determine which items (e.g., words, bigrams, etc.) occur more frequently in the news paper corpus as compared to the fiction corpus. We will start by looking at the words that only occur in the newspaper corpus. As we can see, there are a number of proper nouns (e.g., _kennedy_ and _khrushchev_) along with dates and other words commonly used in newspapers.
```python
brown_key_news_fic = keyness(brown_news_freq,brown_fic_freq) #this will include all of our keyness dictionaries. Note that this is directional (if we switch the frequency dictionaries we will get different but complementary results)
head(brown_key_news_fic["c1_only"],10) #items that only occur in the newspaper corpus (the first frequency list we entered into the keyness() function)
```
```
> kennedy 772.398157358065
per     566.7957701476447
khrushchev      433.4320595246695
1960    333.4092765574381
democratic      311.1819914536089
dallas  305.62517017765157
mantle  300.06834890169426
1961    283.39788507382235
jr      277.84106379786505
laos    272.28424252190774
```
Now, we will look at words that only occur in our corpus of fiction. We see that the most frequent hit is a punctuation mark that we didn't account for.
```python
head(brown_key_news_fic["c2_only"],10)
```
```
> ====    382.79104601814095
bottle  249.64633435965717
shook   216.3601564450362
jess    195.5562952483981
linda   187.23475076974285
kate    183.07397853041525
laughed 178.91320629108762
scotty  178.91320629108762
curt    166.43088957310476
matsuo  153.94857285512194
```
Next, we will look at the top hits for words that are shared across the two corpora using percent difference (%diff). The results indicate (for example) that _administration_ occurs with a frequency that is 10,717% higher in the newspaper corpus than the fiction corpus.
```python
head(brown_key_news_fic["%diff"],10)
```
```
> administration  11652.632544079483
1       10717.764046254979
soviet  10183.553476069548
berlin  8313.816480420537
communist       8180.263837874182
4       7512.500625142393
election        7245.395340049677
international   7111.842697503319
vote    6844.737412410604
industry        6711.184769864246
```
We can also look at the words that occur less frequently in the newspaper corpus than the fiction corpus. The results indicate (for example) that _drink_ has a 97% lower frequency in the newspaper corpus than the fiction corpus.
```python
head(brown_key_news_fic["%diff"],10,hsort = False) #reverse order
```
```
> drink   -97.69736823195935
lips    -97.57177013552077
wondered        -97.15845441390728
horses  -97.15845441390728
nodded  -97.09668168377482
cousin  -96.96471266940095
stairs  -96.82017517746768
ai      -96.82017517746768
hell    -96.43859619876379
silent  -96.3904691203687
```


## Exercises

1. What are the five most frequent quadgrams that only occur in the newspaper corpus? Be sure to report the frequencies.

2. What are the five most frequent quadgrams that only occur in the fiction corpus? Be sure to report the frequencies.

3. What are the ten most "key" trigrams in the newspaper corpus? Be sure to report the keyness values (and method used).

4. What are the ten least "key" trigrams in the newspaper corpus? Be sure to report the keyness values (and method used).

5. Check the frequency of the items identified in Exercise 1 in each corpus. What are some related limitations of the keyness method? How might we mitigate this/these issue(s)? (this was purposefully vague... but think about how frequent an item needs to be across contexts to be both "important" and "useful" - and note that this answer may change depending on purpose). Don't spend too much time on this question!

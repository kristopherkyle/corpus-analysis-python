# Python Exercise 7 (Answers)

## import necessary modules

```python
import operator
import glob
import math
```

## Necessary Functions (from tutorials)

```python
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

def ngrammer(token_list, gram_size, separator = " "):
	ngrammed = [] #empty list for n-grams

	for idx, x in enumerate(token_list): #iterate through the token list using enumerate()

		ngram = token_list[idx:idx+gram_size] #get current word token_list plus words n-words after (this is a list)

		if len(ngram) == gram_size: #don't include shorter ngrams that we would get at the end of a text
			ngrammed.append(separator.join(ngram)) # join the list of ngram items using the separator (by default this is a space), add to ngrammed list

	return(ngrammed) #return list of ngrams

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

def corpus_freq(dir_name,gram_size = 1,separator = " "):
	freq = {} #create an empty dictionary to store the word : frequency pairs

	#create a list that includes all files in the dir_name folder that end in ".txt"
	filenames = glob.glob(dir_name + "/*.txt")

	#iterate through each file:
	for filename in filenames:
		#open the file as a string
		text = open(filename, errors = "ignore").read()
		#tokenize text using our tokenize() function
		tokenized = tokenize(text,gram_size,separator) #use tokenizer indicated in function argument (e.g., "tokenize()" or "ngramizer()")

		#iterate through the tokenized text and add words to the frequency dictionary
		for x in tokenized:
			#the first time we see a particular word we create a key:value pair
			if x not in freq:
				freq[x] = 1
			#when we see a word subsequent times, we add (+=) one to the frequency count
			else:
				freq[x] += 1

	return(freq) #return frequency dictionary

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

## Exercises

** 1. What are the five most frequent quadgrams that only occur in the newspaper corpus? Be sure to report the frequencies.**
```python
brown_news_quad = corpus_freq("brown_press",gram_size = 4) #get quadgram frequency list for brown news corpus
head(brown_news_quad) #check results

brown_fiction_quad = corpus_freq("brown_fiction",gram_size = 4) #get quadgram frequency list for brown fiction corpus
head(brown_fiction_quad) #check results

brown_news_fiction_quad_keyness = keyness(brown_news_quad,brown_fiction_quad) #calculate keyness metrics
head(brown_news_fiction_quad_keyness["c1_only"],hits=5)
```
results:
```

per cent of the 105.7347171596316
to the editor of        100.16973204596678
the editor of the       100.16973204596678
is one of the   100.16973204596678
editor of the inquirer  72.34480647764266
```

**2. What are the five most frequent quadgrams that only occur in the fiction corpus? Be sure to report the frequencies.**

```python
#note, the code above is used here as well
head(brown_news_fiction_quad_keyness["c2_only"],hits=5)
```

results:
```
i m going to    79.17029530520149
the edge of the 75.0034376575593
did nt want to  54.169149419348386
i ve got to     50.002291771706204
the two of them 45.83543412406402
```
**3. What are the ten most “key” trigrams in the newspaper corpus? Be sure to report the keyness values (and method used).**

```python
brown_news_tri = corpus_freq("brown_press",gram_size = 3) #get trigram frequency list for brown news corpus
head(brown_news_tri) #check results

brown_fiction_tri = corpus_freq("brown_fiction",gram_size = 3) #get trigram frequency list for brown fiction corpus
head(brown_fiction_tri) #check results

brown_news_fiction_tri_keyness = keyness(brown_news_tri,brown_fiction_tri) #calculate keyness metrics

head(brown_news_fiction_tri_keyness["%diff"], hits = 10) #get top keyness values using %diff
```


results:
```
the united nations      3105.277473398487
as a result     2971.724245340216
the united states       2971.724245340216
is one of       2838.171017281946
mr and mrs      2704.6177892236756
chairman of the 2437.511333107135
of the american 1903.298420874054
secretary of state      1636.1919647575137
of the united   1569.4153507283784
new york city   1502.6387366992433
```

**4. What are the ten least “key” trigrams in the newspaper corpus? Be sure to report the keyness values (and method used).**

```python
head(brown_news_fiction_tri_keyness["%diff"], hits = 10,hsort = False) #get lowest keyness values using %diff
```


results:
```
for a moment    -96.48544136688761
do nt you       -95.548225731391
i ve got        -95.548225731391
the man s       -94.65787087766918
he had no       -94.19333791051
he had nt       -94.19333791051
you want to     -94.19333791051
the edge of     -93.92939872462408
in the kitchen  -93.32233859708649
but he did      -93.32233859708649
```

**5. Check the frequency of the items identified in Exercise 3 in each corpus. What are some related limitations of the keyness method? How might we mitigate this/these issue(s)? (this was purposefully vague… but think about how frequent an item needs to be across contexts to be both “important” and “useful” - and note that this answer may change depending on purpose). Don’t spend too much time on this question!**

```python
top_hits = ["the united nations","as a result","the united states","is one of","mr and mrs","chairman of the","of the american","secretary of state","of the united","new york city"] #list of top hits

for x in top_hits:
	print(x,"\t","news: ",brown_news_tri[x], "\tfiction: ",brown_fiction_tri[x])
```

results:
```
the united nations       news:  24      fiction:  1
as a result      news:  23      fiction:  1
the united states        news:  92      fiction:  4
is one of        news:  22      fiction:  1
mr and mrs       news:  42      fiction:  2
chairman of the          news:  19      fiction:  1
of the american          news:  15      fiction:  1
secretary of state       news:  13      fiction:  1
of the united    news:  25      fiction:  2
new york city    news:  12      fiction:  1
```

**Question:** In what contexts are these words important? In what contexts might they not be particularly important?

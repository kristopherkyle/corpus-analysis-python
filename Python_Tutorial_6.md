# Python Tutorial 6: Collocation
[Back to Tutorial Index](py_index.md)

(updated 10-14-2020)

Concordancing is a core corpus analysis that is essentially qualitative in nature. One quantitative extension of concordancing is collocation analysis, wherein statistics based on the frequency of cooccurrence are used to highlight linguistic patterns.

In this tutorial, we will build on previously covered corpus analyses, such as [frequency](Python_Tutorial_4.md) and [concordancing](Python_Tutorial_5). However, we will add one more analytical step: The calculation of strength of association statistics.

## Collocation analysis

Our goal will be to create a series of functions that will:
- generate the corpus frequency for all words in a corpus
- generate the corpus frequency for words in a particular lexical context
- calculate statistics that provide information about the strength of association between two lexical items

### Tokenizing
First, we will need to tokenize our texts. In this case, we will use a slightly improved version of the tokenize() function from [Python Tutorial 4](Python_Tutorial_4.md) that includes a more complete list of punctuation marks. We can of course also choose to lemmatize our texts, but for this tutorial we won't do that.

```python
def tokenize(input_string): #input_string = text string
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

	return(tokenized)
```

### Frequency
In [Python Tutorial 4](Python_Tutorial_4.md) we created a frequency function that defined a new dictionary, then added to the newly defined dictionary. In this tutorial, we will modify this slightly by creating a function that updates a pre-existing dictionary instead of creating a new one. This will allow us to easily calculate frequency values for a number of different pieces of a text (e.g., left context, right context, different forms of our search term(s), etc.).

```python
#here we use a version of the freq_simple() function that updates a pre-existing dictionary instead of returning a new dictionary
def freq_update(tok_list,freq_dict): #this takes a list (tok_list) and a dictionary (freq_dict) as arguments
	for x in tok_list: #for x in list
		if x not in freq_dict: #if x not in dictionary
			freq_dict[x] = 1 #create new entry
		else: #else: add one to entry
			freq_dict[x] += 1
```
Below, we use the **_freq_update()_** function with a sample dictionary:

```python
sampd = {"a" : 1} #define dictionary, include one key-value pair
samp_list = ["a","b"] #new list of items
freq_update(samp_list,sampd) #update dictioary based on the new list
```
```
> {'a': 2, 'b': 1}
```

### Calculating context frequency
Now, we will use our **_tokenize()_** and **_freq_update()_** functions, along with pieces of the **_concord()_** and **_concord_regex()_** functions from [Python Tutorial 5](Python_Tutorial_5.md) to create a function that calculates the frequency of all target item hits, collocates in the left context, collocates in the right context, total collocate frequency, and total frequency for all items in a text.

Note that we will use the built-in **_type()_** function, which tells us the Python type (e.g., str, list, int, float) of a particular object. This will allow us to use a single function with targets that are lists OR regular expressions.

Our function **_context_freq()_** will take the follow arguments:
- **_tok_list_** a tokenized list of strings
- **_target_** a list of the target strings (e.g., words) OR a regular expression string
- **_nleft_** length of preceding context (in number of words)
- **_nright_** length of following context (in number of words)

**_context_freq()_** will return a dictionary that consists of five dictionaries:
- **_"left_freq"_** is the frequency of collocates in the left context
- **_"right_freq"_** is the frequency of collocates in the right context
- **_"combined_freq"_** is the frequency of collocates in either context
- **_"target_freq"_** is the frequency of each target hit
- **_"corp_freq"_** is the frequency for all word in the corpus

```python
import re
def context_freq(tok_list,target,nleft = 10,nright = 10):
	left_freq = {} #frequency of items to the left
	right_freq = {} #frequency of items to the right
	combined_freq = {} #combined left and right frequency
	target_freq = {} #frequency dictionary for all target hits
	corp_freq = {} #total frequency for all words

	for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
		freq_update([x],corp_freq) #here we update the corpus frequency for all words. Note that we put x in a one-item list [x] to conform with the freq_update() parameters (it takes as list as an argument)

		hit = False #set Boolean value to False - this will allow us to use a list or a regular expression as a search term
		if type(target) == str and re.compile(target).match(x) != None: #If the target is a string (i.e., a regular expression) and the regular expression finds a match in the string (the slightly strange syntax here literally means "if it doesn't not find a match")
			hit = True #then we have a search hit
		elif type(target) == list and x in target: #if the target is a list and the current word (x) is in the list
			hit = True #then we have a search hit

		if hit == True: #if we have a search hit:

			if idx < nleft: #deal with left context if search term comes early in a text
				left = tok_list[:idx] #get x number of words before the current one (based on nleft)
				freq_update(left,left_freq) #update frequency dictionary for the left context
				freq_update(left,combined_freq) #update frequency dictionary for the all contexts
			else:
				left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)
				freq_update(left,left_freq) #update frequency dictionary for the left context
				freq_update(left,combined_freq) #update frequency dictionary for the all contexts
			t = x
			freq_update([t],target_freq) #update frequency dictionary for target hits; Note that we put x in a one-item list [x] to conform with the freq_update() parameters (it takes as list as an argument)

			right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
			freq_update(right,right_freq) #update frequency dictionary for the right context
			freq_update(right,combined_freq) #update frequency dictionary for the all contexts

	output_dict = {"left_freq" : left_freq,"right_freq" : right_freq, "combined_freq" : combined_freq, "target_freq" : target_freq, "corp_freq" : corp_freq}
	return(output_dict)

```
Now, we will test our function on a sample string, which is an excerpt from the NICT JLE corpus:

```python
sample = """ I look sometimes he rides a bicycle everyday
Yes But I don't know her and XXX05's mother because I have two young two child, but my child is very old tha older than hers child
 I like the exercise  very well  I go to the training gym everyday  But   I  m I take care of two child and my husband After that, I go to the gym and department store, supermarket, and that's all
Yes I  my husband we want to the play golf with family, but I don't like a sports  He said "You should go to the gym"  I go to the gym for five years old
Yes  A little But I cannot play  golf very well
 Once a week I practice  once a week with my sons
 son is thirteen years old
Yes But he plays the golf better than me
 But my husband is best golf  daughter is   my daughter is is  play golf than   sometimes  
"""

#use the context_freq() function to search for collocates of "golf" (with 5 words of left context and 5 words of right context)
golf_freqs = context_freq(tokenize(sample),["golf"],5,5)
print(golf_freqs["target_freq"]) #print the "target_freq" dictionary
print(golf_freqs["left_freq"]) #print the "left_freq" dictionary
```
As we can see below, _golf_ occurs five times in our text. In the left (preceding context), we see that _but_, _is_, and _play_ occur most frequently (three times each).
```
> {'golf': 5}
{'we': 1, 'want': 1, 'to': 1, 'the': 2, 'play': 3, 'little': 1, 'but': 3, 'i': 1, 'cannot': 1, 'yes': 1, 'he': 1, 'plays': 1, 'my': 2, 'husband': 1, 'is': 3, 'best': 1, 'daughter': 1}
```

#### A quick sidebar: The head() function
As we proceed, we will continue to create functions that return one or more dictionaries with words as keys and frequency or strength of association statistics as values. To preview these dictionaries as sorted lists, we could continue to use the **_sorted()_** function and the variations of the **_freq_writer()_** function (from [Python Tutorial 4](Python_Tutorial_4.md)) to preview, save, and disseminate our results. However, in the long run it will be more efficient to make a multipurpose function for completing these tasks. The **_head()_** function below is an extended adaptation of the function with the same name in R.

Our Python version of the **_head()_** function takes six arguments:
- **_stat_dict_** is a dictionary that consist of {string : number} key : value pairs (e.g., a frequency dictionary)
- **_hits_** is the number of items to include (default is top 20 items). If you want to include all items in the corpus, choose a very large number (e.g., 10000000000).
- **_hsort_** is a Boolean value. By default, this is True (and the dictionary is sorted with the highest value first)
- **_output_** is a Boolean value. By default it is False. If True, the function will return a sorted list (instead if just printing it)
- **_filename_** by default is None. If a filename is provided (e.g., results.txt), a list will be written to the working directory.
- **_sep_** is a string. By default, this is a "\t" character. It is only used when lists are written to a file.

By default, the **_head()_** function prints a sorted list of items in the **_stat_dict_**. It can also return a sorted list and/or write the list to a file.

```python
import itemgetter
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

```python
#print top 10 items in the left context dictionary
head(golf_freqs["left_freq"],hits = 10)
```

```
> play    3
but     3
is      3
the     2
my      2
we      1
want    1
to      1
little  1
i       1
```

### Calculating context frequencies for a corpus
We will now update our **_context_freq()_** function so that it will calculate context frequencies (etc.) for an entire function. We will also set some default values to make our function a little easier to use.

We will call our updated function **_corpus_context_freq()_**, which will take the following arguments:
- **_dirname_** this is the name of the folder in which the corpus files reside
- **_tok_list_** a tokenized list of strings
- **_target_** a list of the target strings (e.g., words) OR a regular expression string
- **_nleft_** length of preceding context (in number of words; default value is 5)
- **_nright_** length of following context (in number of words; default value is 5)

**_context_freq()_** will return a dictionary that consists of five dictionaries:
- **_"left_freq"_** is the frequency of collocates in the left context
- **_"right_freq"_** is the frequency of collocates in the right context
- **_"combined_freq"_** is the frequency of collocates in either context
- **_"target_freq"_** is the frequency of each target hit
- **_"corp_freq"_** is the frequency for all word in the corpus

```python
import re
def corpus_context_freq(dir_name,target,nleft = 5,nright = 5): #if we wanted to add lemmatization, we would need to add an argument for a lemma dictinoary
	left_freq = {} #frequency of items to the left
	right_freq = {} #frequency of items occuring to the right
	combined_freq = {} #combined left and right frequency
	target_freq = {} #frequency dictionary for all target hits
	corp_freq = {} #total frequency for all words

	#create a list that includes all files in the dir_name folder that end in ".txt"
	filenames = glob.glob(dir_name + "/*.txt")
	#print(filenames)
	#iterate through each file:
	for filename in filenames:
		#open the file as a string
		text = open(filename, errors = "ignore").read()
		#tokenize text using our tokenize() function
		tok_list = tokenize(text)

		#if we wanted to lemmatize our text, we would use the lemmatize function here

		for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
			freq_update([x],corp_freq) #here we update the corpus frequency for all words. Note that we put x in a one-item list [x] to conform with the freq_update() parameters (it takes as list as an argument)

			hit = False #set Boolean value to False - this will allow us to use a list or a regular expression as a search term
			if type(target) == str and re.compile(target).match(x) != None: #If the target is a string (i.e., a regular expression) and the regular expression finds a match in the string (the slightly strange syntax here literally means "if it doesn't not find a match")
				hit = True #then we have a search hit
			elif type(target) == list and x in target: #if the target is a list and the current word (x) is in the list
				hit = True #then we have a search hit

			if hit == True: #if we have a search hit:

				if idx < nleft: #deal with left context if search term comes early in a text
					left = tok_list[:idx] #get x number of words before the current one (based on nleft)
					freq_update(left,left_freq) #update frequency dictionary for the left context
					freq_update(left,combined_freq) #update frequency dictionary for the all contexts
				else:
					left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)
					freq_update(left,left_freq) #update frequency dictionary for the left context
					freq_update(left,combined_freq) #update frequency dictionary for the all contexts
				t = x
				freq_update([t],target_freq) #update frequency dictionary for target hits; Note that we put x in a one-item list [x] to conform with the freq_update() parameters (it takes as list as an argument)

				right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
				freq_update(right,right_freq) #update frequency dictionary for the right context
				freq_update(right,combined_freq) #update frequency dictionary for the all contexts

	output_dict = {"left_freq" : left_freq,"right_freq" : right_freq, "combined_freq" : combined_freq, "target_freq" : target_freq, "corp_freq" : corp_freq}
	return(output_dict)
```

Now, we will test our function on the Brown corpus (don't forget to set your working directory!):

```python
# search for words that start with "investigat"
brown_context_freq = corpus_context_freq("brown_corpus","investigat.*")
head(brown_context_freq["target_freq"]) #get frequency of various target hits
```
Below, we see that _investigation_ is the most frequent target hit, followed by _investigations_ and _investigated_ (along with others).
```
> investigation   51
investigations  22
investigated    18
investigators   13
investigate     11
investigating   8
investigator    4
investigative   3
investigates    1
```

We can also look at the combined collocate frequency:
```python
#get ten most frequent collocates regardless of context
head(brown_context_freq["combined_freq"],hits = 10)
```
```
> the     192
of      125
and     79
to      76
in      72
a       45
by      28
have    23
as      23
was     22
```
And the left and right context frequencies specifically by using the **_head()_** function with _"left_freq"_ and _"right_freq"_ respectively.

We can also check the overall frequency of words in the corpus:
```python
#get ten most frequent words in the corpus
head(brown_context_freq["corp_freq"],hits = 10)
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

### Strength of association
As we saw in the previous section, the most frequent collocates of forms of investigate were also among the most frequent words in the corpus. In short, the co-occurence of the our target item and these frequent words may be a function of their raw frequencies and may not tell us much about the relationship between the two words specifically.

Next, we will create a function **_soa()_**that calculates the strength of association between items in an attempt to control for the raw frequency of each item in the corpus.

**_soa_** will take two arguments:
- **_freq_dict_** is a dictionary of frequency dictinoaries generated by the **_corpus_context_freq()_** function
- **_cut_off_** is a minimum frequency cut-off for the calculation of strength of association. Any items with frequency values below this number will be ignored. The default value is five.

**_soa_** will return a dictionary of dictionaries that consist of various strength of association measures. These include (see code below for all equations):
- **_"mi"_** Mutual Information (MI) score; highlights restrictive collocations
- **_"tscore"_** T score (T); highlights frequent collocations
- **_"faith_coll_cue"_** Faithfulness; Probability of seeing the target item given the presence of the collocate
- **_"faith_target_cue"_** Faithfulness; Probability of seeing the collocate given the presence of the target item
- **_"deltap_coll_cue"_** Delta P; Probability of seeing the target item given the presence of the collocate MINUS the probability of seeing the target item given the presence of any word other than the collocate
- **_"deltap_target_cue"_** Delta P;Probability of seeing the collocate given the presence of the target item MINUS the probability of seeing the collocate given the presence of any word other than the target item

```python
import math
def soa(freq_dict,cut_off = 5):
	mi = {}
	tscore = {}
	faith_coll_cue = {}
	faith_target_cue = {}
	deltap_coll_cue = {}
	deltap_target_cue = {}

	corpus_size = sum(freq_dict["corp_freq"].values()) #get the size of the corpus by summing the frequency of all words . This will stay consistent for all iterations below
	target_freq = sum(freq_dict["target_freq"].values()) #get the total number of corpus hits for all forms of the target item. This will stay consistent for all iterations below

	#iterate through context hits
	for collocate in freq_dict["combined_freq"]:
		observed = freq_dict["combined_freq"][collocate] #frequency of target coocurring with collocate
		collocate_freq = freq_dict["corp_freq"][collocate] #Total frequency of collocate in corpus

		if freq_dict["combined_freq"][collocate] >= cut_off: #check to make sure that the collocate occurs frequently enough to surpass the threshold
			expected = ((target_freq * collocate_freq)/corpus_size)

			mi[collocate] =  math.log2(observed/expected) #calculate MI score and add it to dict


			tscore[collocate] = (observed-expected)/(math.sqrt(observed)) #calcuate T score and add it to dict

			#	 y  -y
			#	_______
			# x | a | b
			#	 ___|___
			# -x| c | d
			#
			# deltap P(outcome|cue) - P(outcome|-cue)
			# delta P(y|x) = (a/(a+b)) - (c/(c+d))
			# delta P(x|y) = (a/(a+c)) - (b/(b+d))
			#x = collocate
			#y = target
			a = observed
			b = collocate_freq - a
			c = target_freq - a
			d = corpus_size - (a+b+c)

			#finish this!
			faith_coll_cue[collocate] = (a/(a+b)) #P(target | collocate)
			faith_target_cue[collocate] = (a/(a+c)) ##P(collocate | target)

			deltap_coll_cue[collocate] = (a/(a+b)) - (c/(c+d)) #P(target | collocate) - P(target | -collocate)
			deltap_target_cue[collocate] = (a/(a+c)) - (b/(b+d)) #P(collcate | target) - P(collocate | -target)

	#create output dictionary:
	output_dict = {"mi" : mi,"tscore" : tscore, "faith_coll_cue" : faith_coll_cue, "faith_target_cue" : faith_target_cue, "deltap_coll_cue" : deltap_coll_cue, "deltap_target_cue" : deltap_target_cue}
	return(output_dict)
```

Now, we can use our **_soa()_** function to look for collocates of all items that begin with "investigat" using the dictionary (_brown_context_freq_)that we previously generated. We will then look at the lists generated by the various strength of association statistics, starting with MI:

```python
brown_soa = soa(brown_context_freq)
head(brown_soa["mi"],hits = 10)
```
The results indicate that "bureau" is the most strongly associated item (according to MI) score, likely as part of a name (i.e., the Federal Bureau of Investigation; we would need to do a concordance search to check).
```
> bureau  10.49096922934631
original        8.552661551752552
federal 8.29664757359653
report  8.281645410257283
committee       8.109879061990803
city    6.620776576677164
number  6.356519029573929
used    6.247167914950834
other   5.769181163083601
been    5.645770956144033
```
Next, we will take a look at some of the results with regard to T score:
```python
head(brown_soa["tscore"],hits = 10)
```
The T score results highlight frequent collocations such as "the". This may be due to the fact that the most frequent versions of "investigat" were nouns (but again, we need to look at concordance lines to confirm this)
```
the     13.203587775764168
of      10.759308340956522
and     8.468529620947434
to      8.329895145485272
in      8.1601389590553
a       6.259020362668412
by      5.161870288339875
have    4.689569565875919
as      4.6001553312696615
was     4.419892835586372
```
When Faithfulness (collocate cue) is used, we get a list that is identical to that generated by MI for the first ten items (note that this is not always true):

```python
head(brown_soa["faith_coll_cue"],hits = 10)
```
The results here indicate that when "bureau" occurs in the corpus, a form of "investigat" will occur 18.6% of the time.
```
bureau  0.18604651162790697
original        0.04854368932038835
federal 0.04065040650406504
report  0.040229885057471264
committee       0.03571428571428571
city    0.01272264631043257
number  0.01059322033898305
used    0.009819967266775777
other   0.007050528789659225
been    0.006472491909385114
```
When Faithfulness (target cue) is used, we get a list that is identical to that generated by T for the first ten items (note that this is not always true):
```python
head(brown_soa["faith_target_cue"],hits = 10)
```
The results here indicate that when a form of "investigat" occurs in the corpus there is a (somewhat nonsensical) 146.56% chance that "the" will occur. The probability value here is higher than 1 because "the" can occur in the context window more than once!
```
> the     1.465648854961832
of      0.9541984732824428
and     0.6030534351145038
to      0.5801526717557252
in      0.549618320610687
a       0.3435114503816794
by      0.21374045801526717
have    0.17557251908396945
as      0.17557251908396945
was     0.16793893129770993
```

## Exercises

# Python Exercise 8 (Answers)

## Import necessary modules
```python
import glob
import operator
import xml.etree.ElementTree as ET #import ElementTree
```

## Utility functions and annotation extraction (from tutorial):

```python
#utility function:
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

#dicters:
def pos_dicter(text,splitter):
	output_list = [] #list for each token
	tokenized = text.lower().split(" ") #split tokens on white space
	for x in tokenized: #iterate through tokens
		if splitter not in x: #ignore tokens that don't have the tag splitter character (i.e., that don't have tags; this will ignore extra spaces, newline characters, etc.)
			continue
		token = {} #represent each token as a dictionary
		toklist = x.split(splitter) #for each, separate words from tags
		token["word"] = toklist[0] #word
		token["pos"] = toklist[1] #pos tag

		output_list.append(token) #add token dictionary to list

	return(output_list)


def conll_dicter(text,splitter):
	output_list = [] #list for each token
	sent_start = -1 #this is to adjust dependency head references for the whole document
	previous_id = 0

	text = text.split("\n") #split text into lines
	for line in text:
		token = {}
		if len(line) < 1: #skip lines without annotation
			continue
		if line[0] == "#": #skip lines without target annotation
			continue
		anno = line.split(splitter) #split by splitting character (in the case of our example, this will be a tab character)
		if int(anno[0]) == 1:
			sent_start += previous_id #update sent_start
			previous_id = 0 #reset last id
		#now, we will grab all relevant information and add it to our token dictionary:
		token["idx"] = sent_start + int(anno[0])
		token["word"] = anno[1].lower() #put words in lower case
		token["upos"] = anno[3] #get the universal pos tag
		token["pos"] = anno[4] #penn tag
		token["dep"] = anno[7] #dependency relationship
		if token["dep"] == "root": #roots don't have a concrete head. In a sentence, their head idx is 0. That doesn't make sense here, so we will make "root" the head idx.
			token["head_idx"] = "root"
		else:
			token["head_idx"] = sent_start + int(anno[6]) #id of dependency head (in document)
		previous_id += 1		
		output_list.append(token)
	return(output_list)

def bnc_xml_dicter(text,splitter = None): #splitter is not used - it is only here to conform with other tokenizer functions so it will work with corpus_freq()
	out_list = [] ##list for each token
	root = ET.fromstring(text) #starting point in parse tree
	for x in root.iter(tag = "w"): #iterate through the "w" tags
		token = {}

		#in this format, spaces are included in the "w" tag text.
		word = x.text #get word text

		if word == None: #in some cases, <w> tags don't have text.
			continue #we will ignore these
		else:
			word = word.strip() #remove trailing spaces

		token["word"] = word  
		token["lemma"] = x.get("hw") #get lemma from attribute "head"
		token["pos"] = x.get("c5") #get CLAWS 5 POS tag from attribute "c5"
		token["big_pos"] = x.get("pos") #get pos tag from attribute "pos"
		out_list.append(token)
	return(out_list)
```

## Bigram extraction and frequency code (from tutorials):

```python
#bigram extractor
def bigrammer_pos(token_list, pos1, pos2, separator = " "):
	ngrammed = [] #empty list for n-grams

	for idx, x in enumerate(token_list): #iterate through the token list using enumerate()
		if len(token_list) -1 == idx: #if we get to the last word of the text
			continue #don't try to make an bigram

		if x["pos"] in pos1: #first, see if the pos of the node word is in pos1list
			if token_list[idx+1]["pos"] in pos2: #then, see if the pos of the second word (token_list[idx+1]) is in pos2list
				ngram = separator.join([x["word"],token_list[idx+1]["word"]]) #if so, ngram = word1 + word2
				ngrammed.append(ngram) #append to ngrammed list

	return(ngrammed) #return list of ngrams

#frequency compiler
def corpus_freq(dir_name,tokenizer,splitter, pos1, pos2, separator = " ", ending = ".txt"):
	freq = {} #create an empty dictionary to store the word : frequency pairs

	#create a list that includes all files in the dir_name folder that end in ".txt"
	filenames = glob.glob(dir_name + "/*" + ending)

	#iterate through each file:
	for filename in filenames:
		#open the file as a string
		text = open(filename, errors = "ignore").read()
		#tokenize text using our the selected tokenizer function, which may differ based on the format of our data
		tokenized = tokenizer(text,splitter) #use tokenizer indicated in function argument (e.g., "tokenize()" or "ngramizer()")

		const_bigrams = bigrammer_pos(tokenized, pos1, pos2, separator)
		#iterate through the tokenized text and add words to the frequency dictionary
		for x in const_bigrams:
			#the first time we see a particular word we create a key:value pair
			if x not in freq:
				freq[x] = 1
			#when we see a word subsequent times, we add (+=) one to the frequency count
			else:
				freq[x] += 1

	return(freq) #return frequency dictionary
```

## Exercises

NOTE: Make sure that the appropriate corpus files are in your working directory!!!

**1. Using the functions defined in this tutorial, find and report the 10 most frequent adverb + adjective combinations in the Brown corpus, the GUM corpus, and the BNC Baby corpus. Note that you will need to check the documentation for each tagset to ensure that you are searching for the correct tags.**

#### Brown:

```python
brown_rb_jj_freq = corpus_freq("brown_pos",pos_dicter,"/", ["rb","rbr","rbt","rn","rp"], ["jj","jjr","jjs","jjt"]) #brown tags
head(brown_rb_jj_freq,hits = 10)
```

```
only natural    7
also possible   6
still alive     6
no such 4
only possible   4
up new  4
also available  4
never sure      4
mentally ill    3
down long       3
```

#### GUM:
```python
gum_rb_jj_freq = corpus_freq("gum_corpus",conll_dicter,"\t", ["RB","RBR","RBS"], ["JJ","JJR","JJS"],ending = ".conllu")
head(gum_rb_jj_freq,hits = 10)
```

```
most popular    6
most important  6
most beautiful  5
very important  5
most successful 4
more likely     4
too many        4
less likely     4
so many 4
much easier     4
```

#### BNC:

```python
bnc_rb_jj_freq = corpus_freq("bnc_baby",bnc_xml_dicter,"\t", ["AV0","AVP","AVQ"], ["AJ0","AJC","AJS"],ending = ".xml")
head(bnc_rb_jj_freq,hits = 10)
```

```
very good       295
very nice       166
more likely     148
most important  123
too bad 82
very different  78
quite good      76
quite nice      73
as good 70
more important  70
```

**2. Adapt your functions to report the 10 most frequent verbs in the Brown Corpus, the GUM corpus, and the BNC Baby corpus. You should be able to do so by making the bigrammer_pos() function return verbs instead of bigrams. This should only require some small changes.**

Note. There are at least two ways to approach this. The method that takes the least effort is to simply modify and redefine your bigrammer_pos() function (note that you will have dummy/un-used variables). The second method is to rename the bigrammer_pos() function and only require the needed arguments. You would then need to change the corpus_freq() function accordingly.

```python
def bigrammer_pos(token_list, pos1, pos2, separator = " "):
	ngrammed = [] #empty list for n-grams

	for idx, x in enumerate(token_list): #iterate through the token list using enumerate()
		if len(token_list) -1 == idx: #if we get to the last word of the text
			continue #don't try to make an bigram

		if x["pos"] in pos1: #first, see if the pos of the node word is in pos1list
			ngrammed.append(x["word"]) #append to ngrammed list

	return(ngrammed) #return list of ngrams
```

#### Brown:

```python
#note: don't forget the separate tags for forms of "to be"!
brown_verb_freq = corpus_freq("brown_pos",pos_dicter,"/", ["vb","vbd","vbg","vbn","vbz","md","be","bed","bedz","beg","bem","ben","ber","bez"], [],ending = ".txt") #brown tags
head(brown_verb_freq, hits = 10)
```

```
is      10003
was     9775
be      6336
are     4334
were    3278
would   2682
been    2470
will    2109
said    1943
can     1736
```

#### GUM:
```python
gum_verb_freq = corpus_freq("gum_corpus",conll_dicter,"\t", ["VB","VBD","VBG","VBN","VBP","VBZ","MD"], [],ending = ".conllu") #penn tags
head(gum_verb_freq, hits = 10)
```
```
is      994
was     719
are     483
be      427
have    371
do      281
can     269
has     238
were    223
had     216
```

#### BNC:
```python
bnc_verb_freq = corpus_freq("bnc_baby",bnc_xml_dicter,"\t", ["VBB","VBD","VBG","VBI","VBN","VBZ","VDB","VDD","VDG","VDI","VDN","VDZ","VHB","VHD","VHG","VHI","VHN","VHZ","VM0","VVB","VVD","VVG","VVI","VVN","VVZ"], [],ending = ".xml") #claws5 tags
head(bnc_verb_freq, hits = 10)
```

```
is      38889
was     36662
's      31015
be      24669
have    22233
had     19293
do      17953
are     17599
said    12860
were    11228
```


**3. Norm your verb frequencies per million words (word frequency/corpus size) * 1000000. For the purposes of this exercise, you can use the following corpus sizes: Brown = 1,000,000; GUM = 113,000; BNC Baby = 4,000,000. What similarities/differences do you observe in the normalized frequencies? Why do you think these similarities/differences exist?**

You don't have to write a function for this, but following DRY (don't repeat yourself) principles, I create one below:

```python
def freq_norm(freq_d,corp_size): #frequency dictionary, size of corpus (integer or float)
	normed = {} #dictionary if normed values

	for x in freq_d: #iterate through dictionary
		normed[x] = (freq_d[x]/corp_size) *1000000 #assign normed value too each key in original dictionary

	return(normed) #return normed frequency dictionary
```

Then, we use the dictionaries defined in Exercise 2:

#### Brown:
```python
brown_verb_freq_norm = freq_norm(brown_verb_freq,1000000)
head(brown_verb_freq_norm,hits = 10)
```
```
is      10003.0
was     9775.0
be      6336.0
are     4334.0
were    3278.0
would   2682.0
been    2470.0
will    2109.0
said    1943.0
can     1736.0
```

#### GUM:
```python
gum_verb_freq_norm = freq_norm(gum_verb_freq,113000)
head(gum_verb_freq_norm,hits = 10)
```

```
is      8796.46017699115
was     6362.83185840708
are     4274.33628318584
be      3778.761061946903
have    3283.185840707965
do      2486.7256637168143
can     2380.5309734513276
has     2106.1946902654868
were    1973.4513274336282
had     1911.504424778761
```
#### BNC:
```python
bnc_verb_freq_norm = freq_norm(bnc_verb_freq,4000000)
head(bnc_verb_freq_norm,hits = 10)
```

```
is      9722.25
was     9165.5
's      7753.75
be      6167.25
have    5558.25
had     4823.25
do      4488.25
are     4399.75
said    3215.0
were    2807.0
```

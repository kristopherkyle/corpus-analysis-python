# Python Tutorial 5: Concordancing
[Back to Tutorial Index](py_index.md)

(updated 10-13-2020)

A central aspect of corpus analysis is examining the contexts in which linguistic items occur (this is referred to as concordancing). With large corpora (and/or with frequently occurring items), a random sample of item occurrences is used.

In order to generate concordance lines, we will need to create a function that:
- can identify target linguistic items and their context
- can create a random sample of the identified items (and context)

We will also need to write concordance lines to a file (for further analysis and record keeping purposes).

## Random sampling in Python
First we will import the Python module [**_random_**](https://docs.python.org/3/library/random.html):
```python
import random
```

We can use the **_random_** module to generate a random sample of items from a population. Below, we will use the function **_random.sample()_** which takes a list of items to sample from and the number of desired samples as arguments.

Note that the Python random number generator will (by default) use the current time as a seed for random number generation. This means that each time you generate a set of random numbers (or in our case a random sample of concordance hits) you will get a different result. In order to make random sampling replicable, we can manually set the seed for the random generator using the **_random.seed()_** function.

```python
random.seed(1) #set seed to 1
sample_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] #sample list to sample from

r_samp = random.sample(sample_list,5) #get a random sample from sample_list with five hits
print(r_samp)
```
```
> [5, 19, 3, 9, 4]
```

## Generating concordance lines

To generate concordance lines we will need to:
- search for target linguistic items (e.g., words)
- get the preceding context for each linguistic item
- get the following context for each linguistic item
- return all hits as a list of lists

There are many ways in which we can accomplish this task. In this case, we will create a function that takes the following arguments:
- **_tok_list_** a tokenized list of strings
- **_target_** a list of the target strings (e.g., words)
- **_nleft_** length of preceding context (in number of words)
- **_nright_** length of following context (in number of words)

```python
def concord(tok_list,target,nleft,nright):
	hits = [] #empty list for search hits

	for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
		if x in target: #if the item matches one of the target items
			t = x #set t as the item

			if idx < nleft: #deal with left context if search term comes early in a text
				left = tok_list[:idx] #get x number of words before the current one (based on nleft)
			else:
				left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)

			right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
			hits.append([left,t,right]) #append a list consisting of a list of left words, the target word, and a list of right words

	return(hits)
```
Below, we will test our function using a sample list. We will search for hits of the word "pizza", and will include five items of left and right context.

```python
sample_list = "If I had to name my favorite food it would be pepperoni pizza . I really love to eat pizza because it is nutritious and delicious .".lower().split(" ")

samp_hits = concord(sample_list,["pizza"],5,5) #note that our target is in a list!!!

for x in samp_hits:
	print(x)
```
```
> [['food', 'it', 'would', 'be', 'pepperoni'], 'pizza', ['.', 'i', 'really', 'love', 'to']]
[['i', 'really', 'love', 'to', 'eat'], 'pizza', ['because', 'it', 'is', 'nutritious', 'and']]
```

Now, we will use our integrate our concord function into a larger function **_corp_conc()_** that reads files, tokenizes them, generates a concordance list, and outputs a random sample. **_corp_conc()_** takes the following arguments:

- **_corp_folder_** name of folder that includes the corpus files (this should be in your working directory!)
- **_target_** a list of the target strings (e.g., words)
- **_nhits_** number of samples to include in your random sample
- **_nleft_** length of preceding context (in number of words)
- **_nright_** length of following context (in number of words)

We will also use our tokenize() function from [Python Tutorial 4](Python_Tutorial_4.md)

```python
import glob
import random
random.seed(1) #set seed

def tokenize(input_string):
	tokenized = [] #empty list that will be returned
	punct_list = [".", "?","!",",","'"] #this is a sample (but incomplete!) list of punctuation characters
	replace_list = ["\n","\t"] #this is a sample (but potentially incomplete) list of items to replace with spaces
	ignore_list = [""] #This is a sample (but potentially incomplete) list if items to ignore

	for x in punct_list: #iterate through the punctuation list and replace each item with a space + the item
		input_string = input_string.replace(x," " + x)

	for x in replace_list: #iterate through the replace list and replace it with a space
		input_string = input_string.replace(x," ")

	input_string = input_string.lower() #our examples will be in English, so for now we will lower them

	input_list = input_string.split(" ") #then we split the string into a list

	#finally, we ignore unwanted items
	for x in input_list:
		if x not in ignore_list: #if item is not in the ignore list
			tokenized.append(x) #add it to the list "tokenized"

	#Then, we return the list
	return(tokenized)

def corp_conc(corp_folder,target,nhits,nleft,nright):
	hits = []

	filenames = glob.glob(corp_folder + "/*.txt") #make a list of all .txt file in corp_folder
	for filename in filenames: #iterate through filename
		text = tokenize(open(filename).read())
		#add concordance hits for each text to corpus-level list:
		for x in concord(text,target,nleft,nright): #here we use the concord() function to generate concordance lines
			hits.append(x)

	# now we generate the random sample
	if len(hits) <= nhits: #if the number of search hits are less than or equal to the requested sample:
		print("Search returned " + str(len(hits)) + " hits.\n Returning all " + str(len(hits)) + " hits")
		return(hits) #return entire hit list
	else:
		print("Search returned " + str(len(hits)) + " hits.\n Returning a random sample of " + str(nhits) + " hits")
		return(random.sample(hits,nhits)) #return the random sample
```
Now, we will test our corp_conc() by searching for a random sample of 25 hits for forms of the word "investigate" in the Brown corpus. We will include context of 5 items to the right and 5 items to the left.

```python
target_list = ["investigate","investigates","investigated","investigating","investigation","investigations"]

investigate_conc_25 = corp_conc("brown_corpus",target_list,25,5,5)

for x in investigate_conc_25:
	print(x)

```
```
>Search returned 111 hits.
Returning a random sample of 25 hits

>[['to', 'the', 'press', 'during', 'its'], 'investigation', ['.', 'you', 'know', 'bang-jensen', 'was']]
[[';', ';', 'but', 'on', 'further'], 'investigation', [',', 'the', 'thing', 'proved', 'to']]
[['respect', 'to', 'the', 'variable', 'being'], 'investigated', [':', 'the', 'degree', 'of', 'structure']]
[['76', 'out-of-state', 'visitors', 'interested', 'in'], 'investigating', ['rhode', 'island', "'s", 'industrial', 'advantages']]
[['must', 'be', 'stained', 'for', 'microscopic'], 'investigation', ['.', 'this', 'stain', 'often', 'disrupts']]
[['impurity-doped', 'germanium', 'resistors', 'have', 'been'], 'investigated', ['for', 'use', 'as', 'precision', 'secondary']]
[['tank', 'and', 'went', 'down', 'to'], 'investigate', ['while', 'greg', 'covered', 'him', '.']]
[['official', 'statistics', '.', 'a', 'massive'], 'investigation', ['of', 'the', 'characteristics', 'of', 'in-migrants']]
[['clearly', 'indicate', 'what', 'thorough', 'phonologic'], 'investigation', ['can', 'contribute', 'to', 'orthography', 'design']]
[['took', 'nearly', 'a', 'month', 'to'], 'investigate', [',', 'marshal', 'statistics', ',', 'and']]
[[';', 'therefore', ',', 'in', 'the'], 'investigation', ['of', 'the', 'present', 'hypothesis', ',']]
[['got', 'curious', 'and', 'came', 'to'], 'investigate', ['.', 'once', 'more', 'he', 'lifted']]
[['in', 'your', 'newspapers', ',', 'suggesting'], 'investigation', ['of', 'a', 'common', 'rubbish', 'disposal']]
[['j', '.', 'nunes', ',', 'who'], 'investigated', [',', 'said', 'the', 'thieves', 'broke']]
[['.', 'madden', ',', 'with', 'his'], 'investigation', ['centered', 'on', 'the', 'fraud', ',']]
[['generalists', 'and', 'specialists', 'can', 'be'], 'investigated', ['on', 'a', 'communicative', 'network', 'basis']]
[[')', 'fishery', 'habitat', 'surveys', 'and'], 'investigations', ['on', 'the', '81', ',000', 'miles']]
[['.', 'with', 'its', 'power', 'to'], 'investigate', [',', 'the', 'senate', 'can', 'paralyze']]
[['similar', 'services', '.', 'a', 'little'], 'investigation', ['by', 'telephone', 'or', 'reading', 'the']]
[['previously', 'used', 'for', 'the', 'supplementary'], 'investigations', ['carried', 'out', 'in', 'connection', 'with']]
[['of', 'feed', 'states', 'must', 'be'], 'investigated', ['to', 'allow', 'for', 'interpolation', ';']]
[[',', 'are', 'being', 'characterized', 'and'], 'investigated', ['spectrally', 'in', 'the', 'ultraviolet', 'region']]
[['private', 'eye', 'ends', 'up', 'by'], 'investigating', ['and', 'solving', 'a', 'crime', ',']]
[['vein', 'of', 'philosophical', 'and', 'logical'], 'investigation', ['.', '(', 'cf', '.', 'brodbeck']]
[['unless', 'there', 'was', 'a', 'police'], 'investigation', ["'", "'", '.', '``', 'yeah']]
```
## Sorting concordance lines

If desired, we can also sort our sample alphabetically by target item using the [sorted() function:](https://docs.python.org/3/howto/sorting.html#key-functions)

```python
investigate_conc_25_tsorted = sorted(investigate_conc_25,key = lambda x: x[1]) #sort alphabetically by the target item (x[1])

for x in investigate_conc_25_tsorted:
	print(x)
```
```
> [['tank', 'and', 'went', 'down', 'to'], 'investigate', ['while', 'greg', 'covered', 'him', '.']]
[['introduction', '.', 'in', '1', 'we'], 'investigate', ['a', 'new', 'series', 'of', 'line']]
[['mexican', 'border', 'in', '1916', 'to'], 'investigate', ['lurid', 'newspaper', 'stories', 'about', 'lack']]
[['processes', 'have', 'not', 'been', 'sufficiently'], 'investigated', ['for', 'this', 'population', 'to', 'permit']]
[['probably', 'has', 'never', 'been', 'seriously'], 'investigated', [',', 'although', 'one', 'frequently', 'hears']]
[['of', 'potential', 'builders', 'have', 'been'], 'investigated', [',', 'but', 'none', 'have', 'been']]
[[',', 'two', 'years', '.', 'klauber'], 'investigated', ['the', 'rattlesnakes', 'carefully', 'himself', 'and']]
[['this', 'phenomenon', 'has', 'been', 'experimentally'], 'investigated', ['in', 'detail', 'by', 'maecker', '(']]
[['phosphines', 'and', 'arsines', 'are', 'being'], 'investigated', ['(', 'r', '.', 'g', '.']]
[['coating', 'applications', ',', 'is', 'being'], 'investigated', ['.', 'on', 'the', 'following', 'pages']]
[['fundamental', 'question', 'through', 'a', 'detailed'], 'investigation', ['of', 'the', 'patient', "'s", 'ability']]
[['the', 'original', 'federal', 'bureau', 'of'], 'investigation', ['reports', 'to', 'the', 'department', 'of']]
[['itself', 'a', '``', 'committee', 'of'], 'investigation', ["'", "'", '.', 'in', 'the']]
[[',', 'the', 'federal', 'bureau', 'of'], 'investigation', ['identified', 'the', 'krogers', 'as', 'morris']]
[['he', 'decided', ',', 'if', 'his'], 'investigation', ['of', 'the', 'fraud', ',', 'with']]
[['evidence', 'the', 'federal', 'bureau', 'of'], 'investigation', ['reports', 'might', 'disclose', '.', 'section']]
[['that', 'she', 'would', 'launch', 'an'], 'investigation', ['.', 'he', 'judged', 'her', 'to']]
[[';', ';', 'but', 'on', 'further'], 'investigation', [',', 'the', 'thing', 'proved', 'to']]
[['similar', 'services', '.', 'a', 'little'], 'investigation', ['by', 'telephone', 'or', 'reading', 'the']]
[['10', 'witnesses', 'yesterday', 'in', 'an'], 'investigation', ['of', 'the', 'affairs', 'of', 'ben']]
[['to', 'the', 'personality', 'variables', 'under'], 'investigation', ['.', 'rating', 'scale', 'of', 'compulsivity']]
[['grand', 'jury', 'said', 'friday', 'an'], 'investigation', ['of', 'atlanta', "'s", 'recent', 'primary']]
[['and', 'microcytochemistry', ';', ';', 'the'], 'investigation', ['of', 'the', 'relationship', 'of', 'diphosphopyridine']]
[['.', 'madden', ',', 'with', 'his'], 'investigation', ['centered', 'on', 'the', 'fraud', ',']]
[['a', 'direct', 'replication', 'of', 'their'], 'investigations', [',', 'the', 'results', 'do', 'not']]
```

We can also sort our sample by a particular position in our left or right context. In the example below, we will sort our sample alphabetically by the word immediately preceding our target word.

```python
#sort alphabetically by last item in the left context (x[0][-1]) (i.e., the first word to the left of the target item)
#to sort by the second word to the left of the target item, we would use key = lambda x: x[0][-2]
#to sort by the word immediately to to the right of the target item, we would use key = lambda x: x[2][0]
investigate_conc_25_l1_sorted = sorted(investigate_conc_25,key=lambda x: x[0][-1]) #

for x in investigate_conc_25_l1_sorted:
	print(x)
```
```
[['man', 'and', 'animals', ';', ';'], 'investigation', ['of', 'respiratory', 'diseases', 'of', 'laboratory']]
[['their', 'house', 'in', 'catatonia', 'after'], 'investigating', ['all', 'the', 'regions', 'of', 'suburbia']]
[['grand', 'jury', 'said', 'friday', 'an'], 'investigation', ['of', 'atlanta', "'s", 'recent', 'primary']]
[['generalists', 'and', 'specialists', 'can', 'be'], 'investigated', ['on', 'a', 'communicative', 'network', 'basis']]
[['she', 'approached', 'the', 'problem', 'by'], 'investigating', ['the', 'methods', 'of', 'sound', 'reproduction']]
[['private', 'eye', 'ends', 'up', 'by'], 'investigating', ['and', 'solving', 'a', 'crime', ',']]
[['persons', 'involved', 'in', 'the', 'election'], 'investigation', [',', 'questioned', 'the', 'individuals', 'in']]
[['brought', 'on', 'state', 'and', 'federal'], 'investigations', ['.', 'and', 'the', 'election', 'of']]
[['inquiries', ',', 'supposedly', 'involving', 'field'], 'investigations', [',', 'were', 'conducted', 'in', 'selected']]
[['staff', 'had', 'conducted', 'intensive', 'field'], 'investigations', ['to', 'determine', 'changes', 'in', 'population']]
[['.', 'the', 'first', 'diatomic', 'hydride'], 'investigated', ['by', 'the', 'paramagnetic', 'resonance', 'method']]
[['philadelphia', 'transportation', 'co', '.', 'is'], 'investigating', ['the', 'part', 'its', 'organization', 'played']]
[['to', 'the', 'press', 'during', 'its'], 'investigation', ['.', 'you', 'know', 'bang-jensen', 'was']]
[[',', 'two', 'years', '.', 'klauber'], 'investigated', ['the', 'rattlesnakes', 'carefully', 'himself', 'and']]
[['of', 'the', 'federal', 'bureau', 'of'], 'investigation', ['as', 'to', 'his', 'claim', '.']]
[['tikopia', ',', 'and', 'no', 'senatorial'], 'investigation', ['will', 'result', '.', 'who', 'cares']]
[['processes', 'have', 'not', 'been', 'sufficiently'], 'investigated', ['for', 'this', 'population', 'to', 'permit']]
[['and', 'microcytochemistry', ';', ';', 'the'], 'investigation', ['of', 'the', 'relationship', 'of', 'diphosphopyridine']]
[['a', 'direct', 'replication', 'of', 'their'], 'investigations', [',', 'the', 'results', 'do', 'not']]
[['attorney', 'general', 'is', 'directed', 'to'], 'investigate', ['.', 'washington', ',', 'june', '18']]
[['tank', 'and', 'went', 'down', 'to'], 'investigate', ['while', 'greg', 'covered', 'him', '.']]
[['.', 'with', 'its', 'power', 'to'], 'investigate', [',', 'the', 'senate', 'can', 'paralyze']]
[['selectmen', 'appoint', 'a', 'committee', 'to'], 'investigate', ['and', 'report', 'on', 'the', 'feasibility']]
[['took', 'nearly', 'a', 'month', 'to'], 'investigate', [',', 'marshal', 'statistics', ',', 'and']]
[['mexican', 'border', 'in', '1916', 'to'], 'investigate', ['lurid', 'newspaper', 'stories', 'about', 'lack']]
```

Finally, we can also do multiple sorts. In the following example, we sort by the node word (x[1], and then by the first word to the left (x[0][-1]). Note that when we do multiple sorts, we have to include our sorts in order and inside a tuple.

```python
investigate_two_sorts = sorted(investigate_conc_25,key=lambda x: (x[1], x[0][-1]))

for x in investigate_two_sorts:
	print(x)
```
```
> [['tank', 'and', 'went', 'down', 'to'], 'investigate', ['while', 'greg', 'covered', 'him', '.']]
[['mexican', 'border', 'in', '1916', 'to'], 'investigate', ['lurid', 'newspaper', 'stories', 'about', 'lack']]
[['introduction', '.', 'in', '1', 'we'], 'investigate', ['a', 'new', 'series', 'of', 'line']]
[['of', 'potential', 'builders', 'have', 'been'], 'investigated', [',', 'but', 'none', 'have', 'been']]
[['phosphines', 'and', 'arsines', 'are', 'being'], 'investigated', ['(', 'r', '.', 'g', '.']]
[['coating', 'applications', ',', 'is', 'being'], 'investigated', ['.', 'on', 'the', 'following', 'pages']]
[['this', 'phenomenon', 'has', 'been', 'experimentally'], 'investigated', ['in', 'detail', 'by', 'maecker', '(']]
[[',', 'two', 'years', '.', 'klauber'], 'investigated', ['the', 'rattlesnakes', 'carefully', 'himself', 'and']]
[['probably', 'has', 'never', 'been', 'seriously'], 'investigated', [',', 'although', 'one', 'frequently', 'hears']]
[['processes', 'have', 'not', 'been', 'sufficiently'], 'investigated', ['for', 'this', 'population', 'to', 'permit']]
[['that', 'she', 'would', 'launch', 'an'], 'investigation', ['.', 'he', 'judged', 'her', 'to']]
[['10', 'witnesses', 'yesterday', 'in', 'an'], 'investigation', ['of', 'the', 'affairs', 'of', 'ben']]
[['grand', 'jury', 'said', 'friday', 'an'], 'investigation', ['of', 'atlanta', "'s", 'recent', 'primary']]
[['fundamental', 'question', 'through', 'a', 'detailed'], 'investigation', ['of', 'the', 'patient', "'s", 'ability']]
[[';', ';', 'but', 'on', 'further'], 'investigation', [',', 'the', 'thing', 'proved', 'to']]
[['he', 'decided', ',', 'if', 'his'], 'investigation', ['of', 'the', 'fraud', ',', 'with']]
[['.', 'madden', ',', 'with', 'his'], 'investigation', ['centered', 'on', 'the', 'fraud', ',']]
[['similar', 'services', '.', 'a', 'little'], 'investigation', ['by', 'telephone', 'or', 'reading', 'the']]
[['the', 'original', 'federal', 'bureau', 'of'], 'investigation', ['reports', 'to', 'the', 'department', 'of']]
[['itself', 'a', '``', 'committee', 'of'], 'investigation', ["'", "'", '.', 'in', 'the']]
[[',', 'the', 'federal', 'bureau', 'of'], 'investigation', ['identified', 'the', 'krogers', 'as', 'morris']]
[['evidence', 'the', 'federal', 'bureau', 'of'], 'investigation', ['reports', 'might', 'disclose', '.', 'section']]
[['and', 'microcytochemistry', ';', ';', 'the'], 'investigation', ['of', 'the', 'relationship', 'of', 'diphosphopyridine']]
[['to', 'the', 'personality', 'variables', 'under'], 'investigation', ['.', 'rating', 'scale', 'of', 'compulsivity']]
[['a', 'direct', 'replication', 'of', 'their'], 'investigations', [',', 'the', 'results', 'do', 'not']]
```

## Concordancing with regular expressions
For some applications, it will make more sense to conduct concordance searches using regular expressions. While a full discussion of regular expressions is beyond the scope of this tutorial, we will use a simple regular expression search using the "." wildcard, which will match any character and the "\*" repeat symbol. So, if we searched for "investig.\*", we would match all words that begin with "investig". We could also use the wildcard at other places in our search string. If we searched for ".\*ation.\*", we would match all words that include the characters "ation" (e.g., "investigation", "recrimination", "deliberations", etc.).

For more on regular expressions, [see the Python documentation for regex](https://docs.python.org/3/howto/regex.html).

In the example below, we only have to change one line to make our function use regular expressions (see the first line in the for loop).

```python
import re #import regular expressions module

def concord_regex(tok_list,target_regex,nleft,nright):
	hits = [] #empty list for search hits

	for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
		if re.compile(target_regex).match(x) != None: #If the target regular expression finds a match in the string (the slightly strange syntax here literally means "if it doesn't not find a match")
			if idx < nleft: #this deals with circumstances where are target word occurs near the beginning of the text
				nleft = idx #if the desired left context is longer than is possible, use as much left context as possible (i.e., to the beginning of the text)
			t = x #set t as the item
			left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)
			right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
			hits.append([left,t,right]) #append a list consisting of a list of left words, the target word, and a list of right words

	return(hits)

sample_list = "If I had to name my favorite food it would be pepperoni pizza . I really love to eat pizza because it is nutritious and delicious .".lower().split(" ")

samp_hits = concord_regex(sample_list,"piz.*",5,5)

for x in samp_hits:
	print(x)
```
```
> [['food', 'it', 'would', 'be', 'pepperoni'], 'pizza', ['.', 'i', 'really', 'love', 'to']]
[['i', 'really', 'love', 'to', 'eat'], 'pizza', ['because', 'it', 'is', 'nutritious', 'and']]
```

## Writing concordance lines to a file
It is likely most convenient to examine concordance lines in spreadsheet software (e.g., using [LibreOffice](https://www.libreoffice.org/) or Excel).

To do so, we will need to convert our concordance lines to strings. In the example below, I will simply create a string that is formatted as left context + tab + target word + tab + right context. However, we could also fairly easily add a tab character between each of the context items (which would allow us to do further sorts in spreadsheet software).

**Don't forget to set your working directory!**

```python
def write_concord(outname, conc_list):
	outf = open(outname,"w")
	outf.write("left_context\tnode_word\tright_context") #write header (optional)
	for x in conc_list:
		left = " ".join(x[0]) #join the left context list into a string using spaces
		target = x[1] #this is the node/target word
		right = " ".join(x[2]) #join the left context list into a string using spaces
		outf.write("\n" + left + "\t" + target + "\t" + right)
	outf.flush()
	outf.close()

write_concord("investigate_conc.txt",investigate_two_sorts)
```
## Exercises

1. Create a sample of 50 concordance lines of the word "record" in the Brown corpus. Use ten words of right context and ten words of left context. Write the concordance lines to a file. Then, read the concordance lines and identify at least two senses of the word "record". Be sure to provide at least two examples of each sense.

2. Update the corp_conc() function in a manner that allows you to use the concord_regex() function instead of the concord() function and call it corp_conc_regex(). Then, create a sample of 50 concordance lines with node/target words that start with "repe". What is the most common root word in your sample?

3. Create a sample of 50 concordance lines that include words with the nominalized suffix "ation" (be sure to include plural forms). Bonus points if you are able to avoid words such as "nation" (which is not a transparent nominalization-don't overthink this).

4. Create a version of the "write_concord()" function that places a tab character between items in the context lists instead of a space. Do a concordance search of your choosing (in Brown or another corpus) and write the concordance lines to a file called "my_search.txt"

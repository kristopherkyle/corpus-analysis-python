# Python Tutorial 9: Extracting Dependency Relations, Calculating Strength of Association
[Back to Tutorial Index](py_index.md)

In this tutorial, we will work more with texts that are tokenized, tagged, and dependency parsed by spaCy.

This tutorial presumes:
1. That you have [installed spaCy](https://spacy.io/usage)
2. That you have installed the ["en_core_web_sm" language model](https://spacy.io/usage/models) for spaCy
3. That you have downloaded [this version of the Brown corpus (which includes 500 files)]((https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Course-Materials/brown_single.zip?raw=true), extracted it, and placed it in your working directory (making sure that you see the text files when you open the folder, not a "\_MacOSX" folder and a "brown_single" folder)

### Extracting dependency relations (dependency bigrams) with spacy

While collocation analyses are very useful in corpus linguistics, it is often helpful to see the grammatical relations between particular words (and determine the strength of association between particular relations).

For example, it may be useful to see all of the collocates of the word "red". However, it may be more useful in many situations to see all of the nouns that tend to be modified by the adjective "red" more specifically. Of course, this all depends on one's research questions.

SpaCy makes it very easy to tag a text for dependency relationships and identify the dependency head (also called a "governor") in each relationship.

```python
import spacy
nlp = spacy.load("en_core_web_sm") #load the English model. This can be changed - just make sure that you download the appropriate model first

sample = "The famous player scored a goal." #sample text

doc = nlp(sample) #tokenize, tag, and parse the sample text

for token in doc: #iterate through processed text
	print(token.lemma_, #print lemma form of word
	token.dep_, #print dependency relationship
	token.head.lemma_) #print the lemma form of the words head (via the dependency relationship)

```

```
>
the det player
famous amod player
player nsubj score
score ROOT score
a det goal
goal dobj score
. punct score
```
If we want to analyze the frequency (or strength of association) of particular pairs of words within a particular dependency relationship (e.g., adjectives and the nouns that they modify), we can do this relatively easily.

The function **_dep_bg_simple()_** below is a simple example of how to create a list of dependency bigrams from a text. The function takes two arguments, namely a text (in the form of a string), and a dependency relationship (in the form of a string).

The function simply parses a string (the **_text_** argument) and determines whether the dependency relationship for each word matches the **_dependent_** argument. If so, the dependent and the head are joined with an underscore ("\_") and added to a list. The program returns a list of all matches.

```python
def dep_bg_simple(text,dependent): #for teaching purposes
	dep_list = [] #list for dependency bigrams
	doc = nlp(text) #tokenize, tag, and parse text

	for token in doc: #iterate through tokens

		if token.dep_ == dependent: #if the dependency relationship matches
			dep = token.lemma_ #extract the lemma of the dependent
			head = token.head.lemma_ #extract the lemma of the head

			dep_bigram = dep + "_" + head #create a dep_head string

			dep_list.append(dep_bigram) #add dep_head string to list

	return(dep_list)
```
Below, the **_dep_bg_simple()_** function is used to find all _amod_ relationships in the sentence "The expensive red car ran into the orange cones."

```python
sample2 = "The expensive red car ran into the orange cones."
sample_amod = dep_bg_simple(sample2,"amod")
print(sample_amod)
```
```
['expensive_car', 'red_car', 'orange_cone']
```
### Calculating Association Strengths (Step 1)

In [Tutorial 6](Python_Tutorial_6), we briefly discussed association strength in terms of pointwise mutual information (MI) and t-score (T). While these are commonly used association strength metrics for collocations, other (perhaps superior, see Gries & Ellis, 2015) metrics are also available such as **_faith_** and **_delta p_**. While MI and T are not directional, **_faith_** and **_delta p_** are (see Gries & Ellis, 2015).

**_Faith_** is simply the probability of an outcome occurring given a particular cue (e.g., the probability of having "car" as an outcome given the word "red"). Faith is directional, meaning that a different value is obtained if we calculate the probability of getting the word "red" given the word "car".

**_delta p_** (or, change in probability) is a variant of Faith that adjusts probability of getting the outcome given a cue by subtracting for the probability of getting the outcome (e.g., car) with any other cue.

In order to calculate association strengths, we need to know the size of the corpus (or in this case, the number of particular dependency relationships we have, e.g., the number of "amod" relationships in a corpus), the frequency of the dependent in the dependency relationship (e.g., the frequency of "red" as an adjective modifier), and the frequency of the head in the dependency relationship (e.g., "car" modified by an adjective).

The function **_dep_bigram_corpus()_** takes a corpus directory/folder as input and returns a dictionary of frequency dictionaries needed to calculate association strengths between dependents and heads of particular dependency relationships. These frequency dictionaries, (which can be accessed with the keys "bi_freq", "dep_freq", and "head_freq") can then be used to calculate association strength using the **_bigram_soa()_** function (which is described in the next section).

The **_dep_bigram_corpus()_** function takes nine arguments (but only the first two need to be specified for the program to run with the default settings).
1. **_dirname_** is a string. This should be the name of the folder that your corpus files are in.
2. **_dep_** is a string. This will indicate the dependency relationship to be examined. Common examples include adjective modifier "amod", direct object "dobj" and noun modifier ("nmod"). A complete list of dependency relationships tagged by spaCy can be found [in the spaCy dependency annotation documentation](https://spacy.io/api/annotation#dependency-parsing).
3. **_ending_** is a string that indicates the file ending for your corpus files. By default, this is ".txt".
4. **_lemma_** is a Boolean value. If True, the word form will be a lemma. Otherwise, the word form will be a word. The default value is True.
5. **_lower_** is a Boolean value. Lemmas are lower case by default in spaCY. If lemma = False and lower = True, the word form will be a word in lower case. The default value is lower = True
6. **_dep_upos_** is a string. If specified, the function will only return hits if the universal part of speech tag for the dependent matches what is provided. Common examples include nouns "NOUN", and adverbs "ADV". A complete list of universal part of speech tags used by spaCy can be found in the [spacy part of speech annotation documentation](https://spacy.io/api/annotation#pos-tagging). By default, this is ignored.
7. **_head_upos_** is a string. If specified, the function will only return hits if the universal part of speech tag for the dependent matches what is provided. Common examples include verbs "VERB", and nouns "NOUN". A complete list of universal part of speech tags used by spaCy can be found in the [spacy part of speech annotation documentation](https://spacy.io/api/annotation#pos-tagging). By default, this is ignored.
8. **_dep_text_** is a string. If specified, the function will only return hits if the dependent token matches what is provided. By default, this is ignored.
9. **_head_text_** is a string. If specified, the function will only return hits if the head token matches what is provided. By default, this is ignored.

```python
def dep_bigram_corpus(dirname,dep,ending = ".txt", lemma = True, lower = True, dep_upos = None, head_upos = None, dep_text = None, head_text = None):
	filenames = glob.glob(dirname + "/*" + ending) #gather all text names

	bi_freq = {} #holder for dependency bigram frequency
	dep_freq = {} #holder for depenent frequency
	head_freq = {} #holder for head frequency
	range_freq = {}
	match_sentences = [] #holder for sentences that include matches

	def dicter(item,d): #d is a dictinoary
		if item not in d:
			d[item] = 1
		else:
			d[item] +=1

	file_count  = 1 #this is to give the user updates about the pogram's progress
	total = len(filenames) #this is the total number of files to process

	for filename in filenames: #iterate through corpus filenames
		#user message
		print("Tagging " + str(file_count) + " of " + str(total) + " files.")
		file_count += 1 #add one to the file_count

		text = open(filename, errors = "ignore").read() #open each file
		doc = nlp(text) #tokenize, tag, and parse text using spaCy
		range_list = [] #for range information
		#sent_text = "first"
		for sentence in doc.sents: #iterate through sentences
			#print(sent_text)
			index_start = 0 #for identifying sentence-level indexes later
			sent_text = [] #holder for sentence
			dep_headi = [] #list for storing [dep,head] indexes
			first_token = True #for identifying index of first token

			for token in sentence: #iterate through parsed spaCy document
				if first_token == True:
					index_start = token.i #if this is the first token, set the index start number
					first_token = False #then set first token to False

				sent_text.append(token.text) #for adding word to sentence

				if token.dep_ == dep: #if the token's dependency tag matches the one designated
					dep_tg = token.pos_ #get upos tag for the dependent (only used if dep_upos is specified)
					head_tg = token.head.pos_ #get upos tag for the head (only used if dep_upos is specified)

					if lemma == True: #if lemma is true, use lemma form of dependent and head
						dependent = token.lemma_
						headt = token.head.lemma_

					if lemma == False: #if lemma is false, use the token form
						if lower == True: #if lower is true, lower it
							dependent = token.text.lower()
							headt = token.head.text.lower()
						else: #if lower is false, don't lower
							dependent = token.text
							headt = token.head.text

					if dep_upos != None and dep_upos != dep_tg: #if dependent tag is specified and upos doesn't match, skip item
						continue

					if head_upos != None and head_upos!= head_tg: #if head tag is specified and upos doesn't match, skip item
						continue

					if dep_text != None and dep_text != dependent: #if dependent text is specified and text doesn't match, skip item
						continue

					if head_text != None and head_text != headt: #if head text is specified and text doesn't match, skip item
						continue

					dep_headi.append([token.i-index_start,token.head.i-index_start]) #add sentence-level index numbers for dependent and head

					dep_bigram = dependent + "_" + headt #create dependency bigram

					range_list.append(dep_bigram) #add to document-level range list
					dicter(dep_bigram,bi_freq) #add values to frequency dictionary
					dicter(dependent,dep_freq) #add values to frequency dictionary
					dicter(headt,head_freq) #add values to frequency dictionary

			### this section is for creating a list of sentences that include our hits ###
			for x in dep_headi: #iterate through hits

				temp_sent = sent_text.copy() #because there may be multiple hits in each sentence (but we only want to display one hit at at time), we make a temporary copy of the sentence that we will modify

				depi = sent_text[x[0]] + "_" + dep+ "_dep" #e.g., word_dobj_dep
				headi = sent_text[x[1]] + "_" + dep+ "_head" #e.g., word_dobj_head

				temp_sent[x[0]] = depi #change dependent word to depi in temporary sentence
				temp_sent[x[1]] = headi ##change head word to headi in temporary sentence

				temp_sent.append(filename) ## add filename to sent to indicate where example originated
				match_sentences.append(temp_sent) #add temporary sentence to match_sentences for output

		for x in list(set(range_list)): #create a type list of the dep_bigrams in the text
			dicter(x,range_freq) #add document counts to the range_freq dictionary


	bigram_dict = {"bi_freq":bi_freq,"dep_freq":dep_freq,"head_freq": head_freq, "range":range_freq, "samples":match_sentences} #create a dictioary of dictionaries
	return(bigram_dict) # return dictionary of dictionaries


```
**Usage examples:**
Note that the dependent of the relationship comes first in the bigram, followed by the head (regardless of their position in a sentence).
```python
#extract all "amod" relationships from the documents in the "brown_single" folder
dobj_brown = dep_bigram_corpus("brown_single","amod")

#import high_val function from corpus_tools (see Tutorial 8)
import from corpus_toolkit import high_val
#get the top 20 bigram frequency hits
high_val(dobj_brown["bi_freq"])
```
Most frequent dependent_head pairs with a "dobj" relationshp (i.e., direct objects and their verbs). As we see below, many of these are pronouns (spaCy lemmatizes all pronouns as "-PRON-")
```
-PRON-_tell     365
what_do 247
-PRON-_see      183
-PRON-_take     159
-PRON-_ask      115
-PRON-_do       106
-PRON-_get      93
-PRON-_put      92
-PRON-_keep     84
place_take      84
```
Frequency of dependents (in this case, lemmas that occur in the direct object position):
```python
high_val(dobj_brown["dep_freq"])
```
```
-PRON-  6060
what    835
that    402
which   335
one     274
man     211
time    206
way     192
hand    190
this    189
```
Frequency of heads (in this case, verb lemmas that take direct objects in the corpus):
```python
high_val(dobj_brown["head_freq"])
```
```
have    2806
take    1298
make    1064
give    997
do      932
see     790
get     661
tell    638
use     496
find    488
```
A random sample of five "dobj" examples (here, we will use Python's **_random_** package to get a random sample from our list of examples):

```python
import random
for example in random.sample(dobj_brown["samples"],5):
	print(" ".join(example).replace("\n",""))
```
```
In a series of fairy tales and fantasies , Melies demonstrated that the film is superbly equipped to tell_dobj_head a straightforward story_dobj_dep , with beginning , middle and end , complications , resolutions , climaxes , and conclusions .  brown_single/cf_cf43.txt
The city sewer maintenance division said efforts will be made Sunday to clear_dobj_head a stoppage_dobj_dep in a sewer connection at Eddy and Elm Streets responsible for dumping raw sewage into the Providence River .  brown_single/ca_ca24.txt
Always troubled by poor circulation in his feet , he experimented with various combinations of socks and shoes before finally adopting_dobj_head old - style_dobj_dep felt farmer 's boots with his sheepskin flying boots pulled over them .  brown_single/cf_cf05.txt
Let me give_dobj_head Papa blood_dobj_dep " .  brown_single/cg_cg54.txt
Early in 1822 he was at Fort Garry offering to bring_dobj_head in pork_dobj_dep , flour , liquor and tobacco .  brown_single/cf_cf17.txt
```

### Calculating Association Strengths (Step 2)

Now that we have calculated the required frequencies, we can calculate various strength of association metrics using the **dep_soa()** function.

The **_bigram_soa()_** function takes a dictionary of frequency dictionaries (such as the one created by the **_dep_bigram_corpus()_**) that includes "bi_freq", "dep_freq", and "head_freq" keys and returns a dictionary of {bigram : soa_value} key : value pairs. The **_bigram_soa()_** takes one required argument and two optional arguments.
1. **_freq_dict_** is a dictionary of frequency dictionaries. The dictionaries must be called using the keys "bi_freq", "dep_freq", and "head_freq". _Note that the association between words in non-dependency bigrams can also be calculated as long as the bigrams in the frequency list are separated with an underscore ("\_"). In this case, "dep_freq" and "head_freq" will point to the same word frequency dictionary._
2. **_stat_** is a string that indicates the association strength calculation method. Choices include "MI", "T", "faith_dep", "faith_head", "dp_dep", and "dp_head". By default, this value is set to "MI"
3. **_range_cutoff_** is an integer that indicates the minimum range threshold for the collocation analysis. If the dependency bigram occurs in fewer corpus documents than the range_cutoff, it will be ignored. The default range_cutoff value is 5.
4. **_cutoff_** is an integer that indicates the minimum frequency threshold for the collocation analysis. If the dependency bigram occurs with a frequency below the cutoff, it will be ignored. The default cutoff value is 5.


```python
def bigram_soa(freq_dict,stat = "MI", range_cutoff = 5, cutoff=5):
	stat_dict = {}
	n_bigrams = sum(freq_dict["bi_freq"].values()) #get number of head_dependent in corpus for statistical calculations

	for x in freq_dict["bi_freq"]:
		observed = freq_dict["bi_freq"][x] #frequency of dependency bigram
		if observed < cutoff:
			continue
		if freq_dict["range"][x] > range_cutoff: #if range value doesn't meet range_cutoff, continue
			continue

		dep = x.split("_")[0] #split bigram into dependent and head, get dependent
		dep_freq = freq_dict["dep_freq"][dep] #get dependent frequency from dictionary

		head = x.split("_")[1] #split bigram into dependent and head, get head
		head_freq = freq_dict["head_freq"][head] #get head frequency from dictionary

		expected = ((dep_freq * head_freq)/n_bigrams) #expected = (frequency of dependent (as dependent of relationship in entire corpus) * frequency of head (of head of relationship in entire corpus)) / number of relationships in corpus

		#for calculating directional strength of association measures see Ellis & Gries (2015)
		a = observed
		b = head_freq - observed
		c = dep_freq - observed
		d = n_bigrams - (a+b+c)

		if stat == "MI": #pointwise mutual information
			mi_score = math.log2(observed/expected) #log base 2 of observed co-occurence/expected co-occurence
			stat_dict[x] = mi_score #add value to dictionary

		elif stat == "T": #t-score
			t_score = math.log2((observed - expected)/math.sqrt(expected))
			stat_dict[x] = t_score

		elif stat == "faith_dep": #probability of getting the head given the governor (e.g., getting "apple" given "red")
			faith_dep_cue = (a/(a+c))
			stat_dict[x] = faith_dep_cue

		elif stat == "faith_head": #probability of getting the head given the governor (e.g., getting "red" given "apple")
			faith_gov_cue = (a/(a+b))
			stat_dict[x] = faith_gov_cue

		elif stat == "dp_dep": #adjusted probability of getting the head given the governor (e.g., getting "apple" given "red")
			delta_p_dep_cue = (a/(a+c)) - (b/(b+d))
			stat_dict[x] = delta_p_dep_cue

		elif stat == "dp_head": #adjusted probability of getting the head given the governor (e.g., getting "red" given "apple")
			delta_p_gov_cue = (a/(a+b)) - (c/(c+d))
			stat_dict[x] = delta_p_gov_cue

	return(stat_dict)
```
**Usage examples:**

Top 10 most strongly associated direct object - verb combinations (using MI):
```python
#get MI values for all dobj relations in the brown corpus
dobj_brown_mi = bigram_soa(dobj_brown)
high_val(dobj_brown_mi,hits = 10)
```

```
radiation_ionize        12.037952463862721
B_paragraph     12.037952463862721
suicide_commit  10.479462174502755
nose_scratch    10.282371191529167
calendar_adjust 9.912421581778862
imagination_capture     9.774918058028927
nose_blow       9.512490974890227
English_speak   9.461760172769297
throat_clear    9.368101065555052
expense_deduct  9.257069753166308
```
Top 10 most strongly associated direct object - verb combinations (using Faith - dependent as cue):
```python
#get MI values for all dobj relations in the brown corpus
dobj_brown_fdep = bigram_soa(dobj_brown,stat = "faith_dep")
high_val(dobj_brown_fdep,hits = 10)
```

```
damn_give       1.0
hereunto_have   1.0
antibody_contain        1.0
incentive_provide       1.0
buffer_start    0.875
chapter_see     0.8461538461538461
suicide_commit  0.8333333333333334
Income_determine        0.8333333333333334
fool_make       0.8333333333333334
dive_make       0.75
```
The results above indicate, for example, that there is a probability of 1.0 (i.e., a 100% chance) that given "damn" as a direct object, the verb will be "give" (in the Brown corpus).

Top 10 most strongly associated direct object - verb combinations (using Faith - head as cue):

```python
#get MI values for all dobj relations in the brown corpus
dobj_brown_mi = bigram_soa(dobj_brown)
high_val(dobj_brown_mi,hits = 10)
```
```
radiation_ionize        1.0
B_paragraph     1.0
-PRON-_distract 0.8333333333333334
-PRON-_frighten 0.7142857142857143
-PRON-_deprive  0.7142857142857143
-PRON-_wake     0.7
-PRON-_wrap     0.625
-PRON-_excuse   0.5555555555555556
-PRON-_mistake  0.5555555555555556
-PRON-_interrupt        0.5454545454545454
```
The results above indicate, for example, that there is a probability of 1.0 (i.e., a 100% chance) that given "ionize" as a verb, the direct object will be "radiation" (in the Brown corpus).

### Bonus: Getting Random Samples and Concordancing with Dependency relations

Often, we will have a large number of hits for the structures we are investigating. In most cases, we will not analyze all of the hits (e.g., if we have 25,000 hits in a large corpus). An alternative method is to take a random sample of hits and analyze those (often between 100 and 500).

Python's **_random.sample()_** function, from the **_random_** package is particularly helpful here. **_random.sample_** will take a list and generate a lists that represents a random sample of _k_ items from the list.

```python
import random
l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
lr = random.sample(l,5)
print(lr)
```
```
[1, 7, 5, 8, 13]
```
By default, the random sample will change each time you run the code. However, you can use the optional **_random.seed()_** function to set the seed (and get the same random sample each time). If you want to get get a different sample after setting the seed, just set it to another number.

```python
l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
random.seed(1)
lr = random.sample(l,5)
print(lr)
```
```
[5, 10, 14, 13, 2]
```

To help the readability of our sample sentences, we will write an .html file using Python's **_ElementTree_** package. We will not dwell on the details here, but will address reading xml files (which are a format related to html) in the next tutorial.

For now, what we need to know is that the "style.text" line below allows us to set the text color for our heads and dependents. For now, these are set as "red" for dependents and "blue" for heads.

The function **_dep_conc()_** below takes four arguments and writes an .html file with the example sentences from a corpus. The resulting .html file can be opened by any web browser.
1. **_example_list_** is a list of sentences that are lists of words, generated by the **_dep_bigram_corpus()_** function.
2. **_hits_** is an integer. It is the number of random samples desired. By default, this is set to 50.
3. **_filename_** is a string representing the name of your output file. By default, this is "results". The suffix ".html" is automatically added to any filename.
4. **_seed_** allows the user to get the same random sample each time (if desired). By default, the seed is set to None, which results in a different sample each time the program is run. Seed can take None or any integer as input.

```python
import xml.etree.ElementTree as ET #for writing xml or html
import random

def dep_conc(example_list,hits = 50, filename = "results",seed = None):
	random.seed(seed) #set seed
	if len(example_list) <= hits: #if the desired number of hits is more than the size of the hit list
		sample_list = example_list #just use the hit list
	else:
		sample_list = random.sample(example_list,hits) #otherwise, produce a random sample

	### This section builds the header material for the .html file.
	outstring = "<!doctype html>\n" ##declare formatting
	root = ET.Element("html") #create root tag
	head = ET.SubElement(root,"head") #create header
	style = ET.SubElement(head,"style") #add style tag
	style.text = "dep {color:red;} \n dep_head {color:blue;}" #set styles for dep and dep_head tags

	#iterate through sentences
	for sentence in sample_list:
		paragraph = ET.SubElement(root,"p") #create new paragraph
		for token in sentence: #iterate through tokens
			if "_dep" in token: #if it is a dependent
				dep = ET.SubElement(paragraph,"dep") #use the dep tag, making it red
				dep.text = token + " " #add the text
			elif "_head" in token: #if it is a head
				dep_head = ET.SubElement(paragraph,"dep_head") #use the dep_head tag, making it blue
				dep_head.text = token + " " #add the text
			else:
				word = ET.SubElement(paragraph,"word") #otherwise, use the word tag (no special formatting)
				word.text = token + " " #add the text

	out_name = filename + ".html" #create filename
	outstring = outstring + ET.tostring(root,method = "html").decode("utf-8") #create output string in correct encoding
	outf = open(out_name, "w") #create file
	outf.write(outstring) #write file
	outf.flush()
	outf.close()
```
**Usage Example**

```python
#create an .html file with 15 hits of dobj relationships from the Brown corpus
dep_conc(dobj_brown["samples"],hits = 15, seed = 12)
```
The following html will be generated (look for a file in your working directory):

<html><head><style>dep {color:red;}
 dep_head {color:blue;}</style></head><p><word>Stammering </word><word>or </word><word>repetition </word><word>of </word><word>I </word><word>, </word><word>you </word><word>, </word><word>he </word><word>, </word><word>she </word><word>, </word><word>et </word><word>cetera </word><word>may </word><dep_head>signal_dobj_head </dep_head><dep>ambiguity_dobj_dep </dep><word>or </word><word>uncertainty </word><word>. </word><word>
 </word><word>brown_single/cf_cf01.txt </word></p><p><word>We </word><dep_head>spend_dobj_head </dep_head><dep>billions_dobj_dep </dep><word>of </word><word>dollars </word><word>at </word><word>the </word><word>race </word><word>tracks </word><word>, </word><word>and </word><word>more </word><word>billions </word><word>on </word><word>other </word><word>forms </word><word>of </word><word>gambling </word><word>. </word><word>
 </word><word>brown_single/cd_cd07.txt </word></p><p><word>Install </word><word>your </word><word>disappearing </word><word>stair </word><word>( </word><word>or </word><word>stairs </word><word>) </word><word>to </word><word>the </word><word>attic </word><word>and </word><word>finish </word><word>your </word><word>overhead </word><word>ducts </word><word>before </word><word>you </word><dep_head>drywall_dobj_head </dep_head><word>the </word><dep>ceiling_dobj_dep </dep><word>. </word><word>
 </word><word>brown_single/ce_ce35.txt </word></p><p><word>Procreation </word><word>, </word><word>expansion </word><word>, </word><word>proliferation </word><word>-- </word><word>these </word><word>are </word><word>the </word><word>laws </word><word>of </word><word>living </word><word>things </word><word>, </word><word>with </word><word>the </word><word>penalty </word><word>for </word><word>not </word><dep_head>obeying_dobj_head </dep_head><dep>them_dobj_dep </dep><word>the </word><word>ultimate </word><word>in </word><word>punishments </word><word>: </word><word>oblivion </word><word>. </word><word>
 </word><word>brown_single/ck_ck23.txt </word></p><p><word>Mr. </word><word>Willis </word><word>, </word><word>eager </word><word>to </word><word>have </word><word>him </word><word>allied </word><word>with </word><word>the </word><word>family </word><word>, </word><dep_head>wanted_dobj_head </dep_head><dep>advice_dobj_dep </dep><word>beyond </word><word>the </word><word>confines </word><word>of </word><word>his </word><word>field </word><word>, </word><word>and </word><word>William </word><word>set </word><word>out </word><word>on </word><word>a </word><word>serious </word><word>study </word><word>of </word><word>the </word><word>situation </word><word>, </word><word>including </word><word>trips </word><word>to </word><word>Wisconsin </word><word>and </word><word>Washington </word><word>. </word><word>
 </word><word>brown_single/cp_cp29.txt </word></p><p><word>" </word><word>I </word><dep_head>see_dobj_head </dep_head><word>your </word><dep>point_dobj_dep </dep><word>, </word><word>Pauson </word><word>. </word><word>
 </word><word>brown_single/cn_cn21.txt </word></p><p><word>And </word><word>though </word><word>in </word><word>his </word><word>later </word><word>years </word><word>he </word><word>revised </word><word>his </word><word>poems </word><word>many </word><word>times </word><word>, </word><word>the </word><word>revisions </word><word>did </word><word>not </word><word>alter </word><word>the </word><word>essential </word><word>nature </word><word>of </word><word>the </word><word>style </word><dep>which_dobj_dep </dep><word>he </word><word>had </word><dep_head>established_dobj_head </dep_head><word>before </word><word>he </word><word>was </word><word>thirty </word><word>; </word><word>; </word><word>so </word><word>that </word><word>, </word><word>while </word><word>it </word><word>usually </word><word>is </word><word>easy </word><word>to </word><word>recognize </word><word>a </word><word>poem </word><word>by </word><word>Hardy </word><word>, </word><word>it </word><word>is </word><word>difficult </word><word>to </word><word>date </word><word>one </word><word>. </word><word>
 </word><word>brown_single/cj_cj65.txt </word></p><p><word>In </word><word>the </word><word>Canadian </word><word>Rockies </word><word>, </word><word>great </word><word>groves </word><word>of </word><word>aspen </word><word>are </word><word>already </word><dep_head>glinting_dobj_head </dep_head><dep>gold_dobj_dep </dep><word>. </word><word>
 </word><word>brown_single/cc_cc15.txt </word></p><p><word>These </word><dep_head>included_dobj_head </dep_head><word>Oregon </word><word>State </word><dep>Fair_dobj_dep </dep><word>, </word><word>for </word><word>which </word><word>he </word><word>had </word><word>been </word><word>booked </word><word>on </word><word>and </word><word>off </word><word>, </word><word>for </word><word>30 </word><word>years </word><word>. </word><word>
 </word><word>brown_single/ca_ca23.txt </word></p><p><word>This </word><word>may </word><word>just </word><word>be </word><word>pride </word><word>in </word><word>my </word><word>adopted </word><word>State </word><word>of </word><word>Washington </word><word>, </word><word>but </word><word>certainly </word><word>I </word><word>love </word><word>to </word><dep_head>visit_dobj_head </dep_head><word>their </word><word>mound </word><dep>cities_dobj_dep </dep><word>near </word><word>Yakima </word><word>and </word><word>Prosser </word><word>in </word><word>July </word><word>or </word><word>August </word><word>, </word><word>when </word><word>the </word><word>bees </word><word>are </word><word>in </word><word>their </word><word>most </word><word>active </word><word>period </word><word>. </word><word>
 </word><word>brown_single/cj_cj10.txt </word></p><p><word>Now </word><word>wait </word><word>a </word><word>minute </word><word>, </word><word>she </word><dep_head>told_dobj_head </dep_head><dep>herself_dobj_dep </dep><word>, </word><word>think </word><word>about </word><word>it </word><word>; </word><word>; </word><word>Lucien </word><word>is </word><word>not </word><word>the </word><word>only </word><word>person </word><word>in </word><word>this </word><word>house </word><word>who </word><word>could </word><word>have </word><word>put </word><word>opium </word><word>in </word><word>that </word><word>coffee </word><word>. </word><word>
 </word><word>brown_single/cl_cl09.txt </word></p><p><word>Occasionally </word><word>he </word><word>would </word><word>look </word><word>across </word><word>the </word><word>aisle </word><word>at </word><word>Margaret </word><word>, </word><word>fourteen </word><word>and </word><word>demure </word><word>in </word><word>a </word><word>fresh </word><word>green </word><word>organdy </word><word>dress </word><word>, </word><word>sitting </word><word>in </word><word>the </word><word>sixth </word><word>- </word><word>grade </word><word>row </word><word>, </word><word>and </word><word>he </word><word>could </word><word>hardly </word><word>believe </word><word>she </word><word>would </word><word>do </word><dep>what_dobj_dep </dep><word>Charles </word><word>had </word><word>said </word><word>she </word><dep_head>did_dobj_head </dep_head><word>. </word><word>
 </word><word>brown_single/cn_cn27.txt </word></p><p><word>All </word><word>these </word><word>materials </word><word>and </word><word>supplementary </word><word>manure </word><word>and </word><word>other </word><word>fertilizers </word><word>from </word><word>neighboring </word><word>dairy </word><word>and </word><word>poultry </word><word>farms </word><dep_head>made_dobj_head </dep_head><word>over </word><word>40 </word><dep>tons_dobj_dep </dep><word>of </word><word>finished </word><word>compost </word><word>a </word><word>year </word><word>. </word><word>
 </word><word>brown_single/cf_cf04.txt </word></p><p><word>The </word><word>primary </word><word>decomposition </word><word>theorem </word><word>We </word><word>are </word><word>trying </word><word>to </word><dep_head>study_dobj_head </dep_head><word>a </word><word>linear </word><dep>operator_dobj_dep </dep><word>T </word><word>on </word><word>the </word><word>finite </word><word>- </word><word>dimensional </word><word>space </word><word>V </word><word>, </word><word>by </word><word>decomposing </word><word>T </word><word>into </word><word>a </word><word>direct </word><word>sum </word><word>of </word><word>operators </word><word>which </word><word>are </word><word>in </word><word>some </word><word>sense </word><word>elementary </word><word>. </word><word>
 </word><word>brown_single/cj_cj18.txt </word></p><p><word>If </word><word>you </word><word>are </word><word>a </word><word>party </word><word>thrower </word><word>, </word><word>you </word><word>may </word><dep_head>need_dobj_head </dep_head><word>added </word><dep>capacity_dobj_dep </dep><word>. </word><word>
 </word><word>brown_single/ce_ce20.txt </word></p></html>

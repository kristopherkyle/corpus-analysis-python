# Python Tutorial 8: Dealing with annotated texts
[Back to Tutorial Index](py_index.md)

(updated 10-22-2020)

Annotating texts for features as part of speech (POS) and syntactic dependency relations (among many, many others) can allow for detailed corpus analyses. For many features (and for many languages), automatic annotation is a viable option (see, e.g., [Spacy](https://spacy.io/), and easy to use POS tagger and dependency parser implemented in Python). However, for some features (and for some languages), automatic annotation tools/models have not been developed (though new NLP tools are being released every day - it is certainly worth a quick web search).

Addtionally, in many cases, corpora have already been annotated for various features (see, e.g., annotated corpora distributed by the [Linguistic Data Consortium](https://catalog.ldc.upenn.edu/topten) and those distributed on the [Universal Dependencies webpage](https://universaldependencies.org/) ).

In this tutorial we will examine three methods of text annotation (and how to deal with annotated texts in Python):
- In-text format
- Vertical format (e.g., CONLL format)
- XML format


## In-text format
Perhaps the simplest form of annotation is in-text annotation, wherein a separator (e.g., "/" or "\_") is used to add annotation (such as part of speech) to a word. Below, we annotate a sentence with POS tags (from the commonly-used [Penn Treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)). In this example, POS tags are separated from words using a "\_" character.

```python
sample1 = "This_DT is_VBZ an_DT example_NN sentence_NN about_IN pepperoni_NN pizza_NN ._."
```
If a text is annotated at the word level, then we can presume that it has already been tokenized (e.g., by white space in the sample above). This means that we can do simple analyses with relatively little effort. For example, we can prepare our sample text for further analysis by lowering the string and then splitting it on white space.

```python
tokenized1 = sample1.lower().split(" ") #lower and then split the sample string
print(tokenized1)
```
```
> ['this_dt', 'is_vbz', 'an_dt', 'example_nn', 'sentence_nn', 'about_in', 'pepperoni_nn', 'pizza_nn', '._.']
```

We can then iterate through a text and focus on particular parts of speech using the **_.split()_** method. In the example below, we print out the word forms for all tokens that have a "dt" (determiner) tag.

```python
for x in tokenized1: #iterate through tokens
	toklist = x.split("_") #for each, separate words from tags
	word = toklist[0] #assign word
	pos = toklist[1] #assign tag
	if pos == "dt":
		print(word)
```
```
> this
an
```
We could also store our annotated text in a Python object (such as a list of lists or a list of dictionaries). Below, we will store our annotated text as a list of dictionaries.
- **_text_** is the input string
- **_splitter_** is the character that separates words from annotations

```python
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
```
```python
sample_posd = pos_dicter(sample1, "_") #create a dictionary representation of each word.
print(sample_posd) #print sample
```
```
> [{'word': 'this', 'pos': 'dt'}, {'word': 'is', 'pos': 'vbz'}, {'word': 'an', 'pos': 'dt'}, {'word': 'example', 'pos': 'nn'}, {'word': 'sentence', 'pos': 'nn'}, {'word': 'about', 'pos': 'in'}, {'word': 'pepperoni', 'pos': 'nn'}, {'word': 'pizza', 'pos': 'nn'}, {'word': '.', 'pos': '.'}]
```
A real-world example is the Brown Corpus, which is available with POS tags (see the [Brown tagset](http://korpus.uib.no/icame/manuals/BROWN/INDEX.HTM) for tag specifications). Tags are separated from words by a "/" character. When used, sub-tags (e.g., "tl") are separated from main tags by a "-" character. You can download the POS-tagged version of the [Brown corpus here]().

```python
brown_sample1 = "The/at Fulton/np-tl County/nn-tl Grand/jj-tl Jury/nn-tl said/vbd Friday/nr an/at investigation/nn of/in Atlanta's/np$ recent/jj primary/nn election/nn produced/vbd ``/`` no/at evidence/nn ''/'' that/cs any/dti irregularities/nns took/vbd place/nn ./."

brown_sample_posd = pos_dicter(brown_sample1, "/") #create a dictionary representation of each word.
print(brown_sample_posd[:5]) #print first 5 words
```
```
> [{'word': 'the', 'pos': 'at'}, {'word': 'fulton', 'pos': 'np-tl'}, {'word': 'county', 'pos': 'nn-tl'}, {'word': 'grand', 'pos': 'jj-tl'}, {'word': 'jury', 'pos': 'nn-tl'}]
```

### Extracting POS-specific bigrams
For practice, we will examine the frequency of adjective-noun combinations using slightly modified versions of our **_ngrammer()_** and **_corp_freq()_** functions from [Python Tutorial 7](Python_Tutorial_7.md). First, we will define a modified version of the **_n\_grammer()_** function, which we will call **_bigrammer_pos()_**.

**_bigrammer_pos()_** takes four arguments (see below) and outputs a list of bigrams that match the search criteria:
- **_token_list_** is a list of token dictionaries with "word" : value and "pos" : value pairs
- **_pos1_** is a list pos tags. The first word in a bigram will have one of these tags
- **_pos2_** is a list pos tags. The second word in a bigram will have one of these tags
- **_separator_** is the character used in a string to separate bigram items. By default, this is " "

```python
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
```
Now, we will test it. We will look for words with adjective tags ["jj","jjr","jjs"] followed by words with common noun tags ["nn","nns"] in our sample. All other word combinations will be ignored.
```python
jj_nn_grams = bigrammer_pos(brown_sample_posd, ["jj","jjr","jjs"], ["nn","nns"], separator = " ")
print(jj_nn_grams)
```
```
> ['recent primary']
```
### Extending analysis to an entire corpus
Now, we will update the **_corpus_freq()_** function to use our new functions (we will also use the **_head()_** function from [Python Tutorial 6](Python_Tutorial_6.md):
**_corpus_freq()_** takes the following arguments:
- **_dir_name_** name of folder that holds our corpus files (don't forget to set your working directory!)
- **_tokenizer_** the name of the tokenizer function to use (we will start by using the pos_dicter() function)
- **_splitter_** is the character that separates words from annotations
- **_pos1_** is a list pos tags. The first word in a bigram will have one of these tags
- **_pos2_** is a list pos tags. The second word in a bigram will have one of these tags
- **_separator_** character (or characters) used to join the n-grams. B7 default this is a space (" ").

```python
import glob
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

Now, we can use **_corpus_freq()_** to determine the frequency of various adjective + noun combinations. As we can see, the most frequent adjective (common) noun combination is _fiscal year_, followed by _high school_, _old man_, and _young man_.

```python
brown_jj_nn_freq = corpus_freq("brown_pos",pos_dicter,"/", ["jj","jjr","jjs"], ["nn","nns"])
head(brown_jj_nn_freq,hits = 10)
```
```
> fiscal year     56
high school     54
old man 52
young man       47
great deal      43
long time       39
young men       29
new members     29
real estate     27
good deal       27
```

## Vertical format (e.g., CONLL format)
While the in-text format can be convenient for simple annotation schemes, more complex annotations schemes require different approaches. One common approach is to list tokens vertically, wherein a text can be read from top to bottom and annotations are provided horizontally.

In other words, each word and its annotations are included in a single (often tab-delimited) row. In this format, hashtags are sometimes used to include metadata.

The example below is taken from the 113,000-word [GUM corpus](https://universaldependencies.org/treebanks/en_gum/index.html) (Zeldes, 2017), which is in [CONLLu format](https://universaldependencies.org/). The format includes the position of the token in the sentence, the token, the lemma, Universal POS tag, Penn POS tag,  detailed grammatical information (left blank for some words), dependency head id, dependency relationship, a blank for additional annotation, and entity information.

In the example below, for example, we see that the word _Therefore_ (position 1, UPOS = ADV, Penn POS = RB) is the dependent of _joined_ (position 4, UPOS = VERB, Penn POS = VBD) via the _advmod_ dependency relationship.

```python
conll_sample = """
# sent_id = GUM_academic_librarians-9
# text = Therefore both institutes joined forces to develop a set of clinics on DH for librarians.
# s_type=decl
1	Therefore	therefore	ADV	RB	_	4	advmod	_	_
2	both	both	DET	DT	_	3	det	_	Entity=(event-50(organization-41
3	institutes	institute	NOUN	NNS	Number=Plur	4	nsubj	_	Entity=organization-41)
4	joined	join	VERB	VBD	Mood=Ind|Tense=Past|VerbForm=Fin	0	root	_	_
5	forces	force	NOUN	NNS	Number=Plur	4	obj	_	_
6	to	to	PART	TO	_	7	mark	_	_
7	develop	develop	VERB	VB	VerbForm=Inf	4	advcl	_	_
8	a	a	DET	DT	Definite=Ind|PronType=Art	9	det	_	Entity=(place-1
9	set	set	NOUN	NN	Number=Sing	7	obj	_	_
10	of	of	ADP	IN	_	11	case	_	_
11	clinics	clinic	NOUN	NNS	Number=Plur	9	nmod	_	_
12	on	on	ADP	IN	_	13	case	_	_
13	DH	DH	PROPN	NNP	Number=Sing	11	nmod	_	Entity=(abstract-2)
14	for	for	ADP	IN	_	15	case	_	_
15	librarians	librarian	NOUN	NNS	Number=Plur	11	nmod	_	Entity=(person-39)event-50)place-1)|SpaceAfter=No
16	.	.	PUNCT	.	_	4	punct	_	_
"""
```

As we did before, we will write a tokenizer function **_conll_dicter()_** to represent CONLL formatted data as a list of dictionaries. In this example, we will not include all of the annotations (though we certainly could).

The **_conll_dicter()_** function takes two arguments (see below) and outputs a list of token dictionaries.
- **_text_** is the input string
- **_splitter_** is the character that separates annotations (in this case, it is "\t")

```python
def conll_dicter(text,splitter):
	output_list = [] #list for each token
	sent_start = -1 #this to adjust token (and head) id numbers in relation to the whole document
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
		token["head_idx"] = sent_start + int(anno[6]) #id of dependency head (in document)
		token["dep"] = anno[7] #dependency relationship
		previous_id += 1		
		output_list.append(token)
	return(output_list)
```
We can test our function on the sample text:
```python
conll_sample_ld = conll_dicter(conll_sample,"\t")
print(conll_sample_ld[:5]) #print the first five items
```
```
> [{'idx': 0, 'word': 'therefore', 'upos': 'ADV', 'pos': 'RB', 'dep': 'advmod', 'head_idx': 3}, {'idx': 1, 'word': 'both', 'upos': 'DET', 'pos': 'DT', 'dep': 'det', 'head_idx': 2}, {'idx': 2, 'word': 'institutes', 'upos': 'NOUN', 'pos': 'NNS', 'dep': 'nsubj', 'head_idx': 3}, {'idx': 3, 'word': 'joined', 'upos': 'VERB', 'pos': 'VBD', 'dep': 'root', 'head_idx': 'root'}, {'idx': 4, 'word': 'forces', 'upos': 'NOUN', 'pos': 'NNS', 'dep': 'obj', 'head_idx': 3}]
```
Now that we have a function that extracts the information we want from CONLL format, we can use the **_bigram_pos()_** and **_corpus_freq()_** functions to calculate adjective-noun bigrams in the GUM corpus. Download the [GUM corpus here](<insert_link>) (don't forget to set your working directory, and note the different filename ending!).

```python
gum_jj_nn_freq = corpus_freq("gum_corpus",conll_dicter,"\t", ["JJ","JJR","JJS"], ["NN","NNS"],ending = ".conllu")
head(gum_jj_nn_freq,hits = 10)
```
```
> early life      11
limited exposure        10
most people     10
first time      10
public domain   9
arrogant people 9
same time       8
19th century    8
digital games   8
other hand      7
```

## XML format
Another popular format for complex annotations is XML (extensive markup language). XML is rather flexible, and can be used to annotate a variety of features in a variety of ways. We will look at a fairly simple example, but XML can be used to include all of the word-level features captured by the CONLL format, and can also be used to easily annotate larger pieces of discourse. XML consists of opening tags "<tag_name>" and closing tags "</tagname>". Tags can have any number of attributes "<tag_name type = "pepperoni"></tagname>", and can also have text (and/or other tags!) between the tags "<tag_name type = "pepperoni">pizza</tagname>"

[BNC Baby](https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2553)
See below for an (abbreviated) sample from the XML version of the [British National Corpus](https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2554). This representation has a number of tags (e.g., \<s> for sentence, \<w> for words). The \<w> tags can have _c5_ ([CLAWS 5 POS tag](http://ucrel.lancs.ac.uk/claws5tags.html)), _hw_ (lemma form), and _pos_ (larger POS category) attributes.

```python
xml_sample = """
<bncDoc >
<s n="18"><w c5="AT0" hw="the" pos="ART">The </w><w c5="NP0" hw="franklin" pos="SUBST">Franklin </w><w c5="NN1" hw="philosophy" pos="SUBST">philosophy </w><w c5="VBD" hw="be" pos="VERB">was </w><w c5="VVN" hw="learn" pos="VERB">learnt </w><w c5="PRP" hw="in" pos="PREP">in </w><w c5="AT0" hw="the" pos="ART">the </w><w c5="NP0" hw="us" pos="SUBST">US </w><w c5="AJ0" hw="leveraged" pos="ADJ">leveraged </w><w c5="NN1" hw="buyout" pos="SUBST">buyout </w><w c5="NN1" hw="business" pos="SUBST">business </w><w c5="PRP" hw="at" pos="PREP">at </w><w c5="AT0" hw="the" pos="ART">the </w><w c5="NN1" hw="side" pos="SUBST">side </w><w c5="PRF" hw="of" pos="PREP">of </w><w c5="NP0" hw="sir" pos="SUBST">Sir </w><w c5="NP0" hw="james" pos="SUBST">James </w><w c5="NN1" hw="goldsmith" pos="SUBST">Goldsmith</w><c c5="PUN">.</c></s>
<s n="19"><w c5="NP0" hw="mr" pos="SUBST">Mr </w><w c5="NP0" hw="franklin" pos="SUBST">Franklin </w><w c5="VVD" hw="go" pos="VERB">went </w><w c5="AV0" hw="there" pos="ADV">there </w><w c5="PRP" hw="at" pos="PREP">at </w><w c5="AT0" hw="the" pos="ART">the </w><w c5="NN1" hw="end" pos="SUBST">end </w><w c5="PRF" hw="of" pos="PREP">of </w><w c5="AT0" hw="the" pos="ART">the </w><w c5="CRD" hw="1970s" pos="ADJ">1970s</w><c c5="PUN">, </c><w c5="PRP" hw="after" pos="PREP">after </w><w c5="AT0" hw="the" pos="ART">the </w><w c5="NN1" hw="collapse" pos="SUBST">collapse </w><w c5="PRF" hw="of" pos="PREP">of </w><w c5="NP0-NN1" hw="keyser" pos="SUBST">Keyser </w><w c5="NP0-NN1" hw="ullman" pos="SUBST">Ullman</w><c c5="PUN">, </c><w c5="AT0" hw="the" pos="ART">the </w><w c5="NN1" hw="merchant" pos="SUBST">merchant </w><w c5="NN1" hw="bank" pos="SUBST">bank </w><w c5="CJS-AVQ" hw="where" pos="CONJ">where </w><w c5="PNP" hw="he" pos="PRON">he </w><w c5="VBD" hw="be" pos="VERB">was </w><w c5="AT0" hw="a" pos="ART">a </w><w c5="NN1" hw="director" pos="SUBST">director </w><w c5="CJT-DT0" hw="that" pos="CONJ">that </w><w c5="VBD" hw="be" pos="VERB">was </w><w c5="VVN" hw="rescue" pos="VERB">rescued </w><w c5="PRP" hw="by" pos="PREP">by </w><w c5="AT0" hw="the" pos="ART">the </w><w c5="NN1" hw="bank" pos="SUBST">Bank </w><w c5="PRF" hw="of" pos="PREP">of </w><w c5="NP0" hw="england" pos="SUBST">England</w><c c5="PUN">.</c></s>
</bncDoc>
"""
```
### Extracting data from XML
The most efficient way to extract information from an XML document is to use an XML parser. There are many XML parsers, but we will use Python's [built-in XML parser ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html), which is easy to use and has great documentation. Below, we will use the **_.iter()_** method to iterate through all \<w> tags in the text. For each \<w> tag, we will use **_.text_** to get text between the opening and closing tags, and **_.get()_** to get attribute values.

```python
import xml.etree.ElementTree as ET #import ElementTree
root = ET.fromstring(xml_sample) #starting point in parse tree
for x in root.iter(tag = "w"): #iterate through the first 10 "w" tags
	word = x.text #get word text
	lemma = x.get("hw") #get lemma from attribute "head"
	pos = x.get("c5") #get CLAWS 5 POS tag from attribute "c5"
	big_pos = x.get("pos") #get pos tag from attribute "pos"
	print(word,lemma,pos,big_pos) #print word, lemma, C5 pos, and big pos
```
(Note, only the first ten lines of the print out are included below - yours will have more lines)
```
> The  the AT0 ART
Franklin  franklin NP0 SUBST
philosophy  philosophy NN1 SUBST
was  be VBD VERB
learnt  learn VVN VERB
in  in PRP PREP
the  the AT0 ART
US  us NP0 SUBST
leveraged  leveraged AJ0 ADJ
buyout  buyout NN1 SUBST
```

### A function to extract data from XML
We will now create a function called **_bnc_xml_dicter()_** to extract token information from BNC texts. As with our previous extraction functions, we will take a text string as input, and return a list of token dictionaries. In this case, our token dictionaries will include the word, lemma, pos tag (CLAWS 5), and big pos tag. If we look closely at the format of the BNC XML files, we see that some whitespace is included for each token. We will clean out this whitespace using the [**_.strip()_**](https://docs.python.org/3/library/stdtypes.html#str.strip) method.

```python
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
Now, we will test our function on our sample xml text:
```python
bnc_sample = bnc_xml_dicter(xml_sample)
for x in bnc_sample[:10]:
	print(x["word"],x["pos"])
```
```
> The AT0
Franklin NP0
philosophy NN1
was VBD
learnt VVN
in PRP
the AT0
US NP0
leveraged AJ0
buyout NN1
```
### Extending the analysis to a corpus
Finally, we can repeat our search for adjective + noun bigrams in a 4-million word sample of the BNC (called BNC Baby). You can download the original [BNC Baby here](https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2553). Our **_corpus_freq()_** function presumes all corpus texts are in the same folder, so we will [use this version](), wherein all corpus .xml files are included in a folder called "bnc_baby". Our analysis indicates that the most frequent adjective + noun combinations are _little bit_, _long time_, and _other hand_ (among many others).

```python
bnc_jj_nn_freq = corpus_freq("bnc_baby",bnc_xml_dicter,"\t", ["AJ0","AJC","AJS"], ["NN0","NN1","NN2"],ending = ".xml")
head(bnc_jj_nn_freq,hits = 10)
```
```
> little bit      246
long time       218
other hand      216
Prime Minister  176
other side      173
other people    165
young people    148
electric field  126
young man       115
front door      115
```

### Sidebar: TEI encoding
One particular type of XML is TEI (text encoding initiative) XML. This type of XML requires a slightly different format, wherein the root tag <TEI> has an attribute that indicates the TEI format version used (e.g., "http://www.tei-c.org/ns/1.0"). For this type of XML, our search for tags looks slightly different. We use the format version identifier (an attribute of the TEI tag) in curly brackets + the desired tag (e.g., "w"). See below for an abbreviated version of this format.

```python
xml_sample2 = """
<TEI xmlns="http://www.tei-c.org/ns/1.0">
<s n="1"><w type="AT">The</w> <w type="NP" subtype="TL">Fulton</w> <w type="NN" subtype="TL">County</w> <w type="JJ" subtype="TL">Grand</w> <w type="NN" subtype="TL">Jury</w> <w type="VBD">said</w> <w type="NR">Friday</w> <w type="AT">an</w> <w type="NN">investigation</w> <w type="IN">of</w> <w type="NPg">Atlanta's</w> <w type="JJ">recent</w> <w type="NN">primary</w> <w type="NN">election</w> <w type="VBD">produced</w> <c type="pct">``</c> <w type="AT">no</w> <w type="NN">evidence</w> <c type="pct">''</c> <w type="CS">that</w> <w type="DTI">any</w> <w type="NNS">irregularities</w> <w type="VBD">took</w> <w type="NN">place</w> <c type="pct">.</c> </s>
</TEI>
"""

root = ET.fromstring(xml_sample2) #starting point in parse tree
for x in root.iter(tag = "{http://www.tei-c.org/ns/1.0}w"): #iterate through all word tags - note the use of {format}+tagname
	word = x.text #get word text
	pos = x.get("type") #get pos tag from attribute "type"
	print(word,pos) #print word and tag
```
```
> The AT
Fulton NP
County NN
Grand JJ
Jury NN
said VBD
Friday NR
an AT
investigation NN
of IN
Atlanta's NPg
recent JJ
primary NN
election NN
produced VBD
no AT
evidence NN
that CS
any DTI
irregularities NNS
took VBD
place NN
```
One example of a corpus that uses TEI XML is the [XML version of the Brown Corpus](). For now, we won't create a function to analyze these texts, but you should be able to do so by making small changes to the **_bnc_xml_dicter()_** function.
## Exercises
1. Using the functions defined in this tutorial, find and report the 10 most frequent adverb + adjective combinations in the Brown corpus, the GUM corpus, and the BNC Baby corpus. Note that you will need to check the documentation for each tagset to ensure that you are searching for the correct tags.

2. Adapt your functions to report the 10 most frequent verbs in the Brown Corpus, the GUM corpus, and the BNC Baby corpus. You should be able to do so by making the **_bigram_pos()_** function return verbs instead of bigrams. This should only require some small changes.

3. Norm your verb frequencies per million words (word frequency/corpus size) * 1000000. For the purposes of this exercise, you can use the following corpus sizes: Brown = 1,000,000; GUM = 113,000; BNC Baby = 4,000,000. What similarities/differences do you observe in the normalized frequencies? Why do you think these similarities/differences exist?

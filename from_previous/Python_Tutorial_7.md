# Python Tutorial 7: Tagging and Parsing Texts with spaCy (and writing tagged corpora)
[Back to Tutorial Index](py_index.md)

The function **_tag()_** takes a string as input (e.g., a text file), and outputs a tokenized and tagged version of the string (as a list of "word_tag" strings). _(Note that the function described in the next section can be used to tag an entire corpus.)_ This function is a wrapper for [spaCy](https://spacy.io/) and presumes that you have [installed spaCy and downloaded the "en_core_web_sm" model](https://spacy.io/usage). Tag takes six arguments.
1. **_text_** is a string (e.g., a corpus document). SpaCy places a limit on string size (1,000,000 characters), so you will want to split up any particularly large strings (files).
2. **_tp_** is a string indicating which type of tag to include. Options are universal POS tags "upos", extended Penn POS tags "penn", and universal dependency tags "dep". The default is "upos"
3. **_lemma_** is a Boolean value. If True, the word form will be a lemma. Otherwise, the word form will be a word. The default value is True.
4. **_lower_** is a Boolean value. Lemmas are lower case by default in spaCY. If lemma = False and lower = True, the word form will be a word in lower case. The default value is lower = True
5. **_connect_** is a string. This is the symbol used to connect the word form and the tag. By default, this is an underscore "_"
6. **_ignore_** is a list of universal POS tags to ignore. By default, this list is ["PUNCT","SPACE","SYM"].


```python
import glob
import spacy #import spacy
nlp = spacy.load("en_core_web_sm") #load the English model. This can be changed - just make sure that you download the appropriate model first

def tag(text,tp = "upos", lemma = True, lower = True, connect = "_",ignore = ["PUNCT","SPACE","SYM"]):

	#check to make sure a valid tag was chosen
	if tp not in ["penn","upos","dep"]:
		print("Please use a valid tag type: 'penn','upos', or 'dep'")
		return #exit the function

	else:
		doc = nlp(text) #use spacy to tokenize, lemmatize, pos tag, and parse the text
		text_list = [] #empty list for output
		for token in doc: #iterate through the tokens in the document
			if token.pos_ in ignore: #if the universal POS tag is in our ignore list, then move to next word
				continue

			if lemma == True: #if we chose lemma (this is the default)
				word = token.lemma_ #then the word form will be a lemma
			else:
				if lower == True: #if we we chose lemma = False but we want our words lowered (this is default)
					word = token.text.lower() #then lower the word
				else:
					word = token.text #if we chose lemma = False and lower = False, just give us the word

			if tp == None: #if tp = None, then just give the tokenized word (and nothing else)
				text_list.append(word)

			else:
				if tp == "penn":
					tagged = token.tag_ #modified penn tag
				elif tp == "upos":
					tagged = token.pos_ #universal pos tag
				elif tp == "dep":
					tagged = token.dep_ #dependency relationship

			tagged_token = word + connect + tagged #add word, connector ("_" by default), and tag
			text_list.append(tagged_token) #add to list

		return(text_list) #return text list
```

Usage examples

Default settings:

```python
#Sample string by HDT in Walden
sample_string = "The cost of a thing is the amount of what I will call life which is required to be exchanged for it, immediately or in the long run."

#using default settings: lemma_upos
tagged_string = tag(sample_string)
print(tagged_string)
```
```
>['the_DET', 'cost_NOUN', 'of_ADP', 'a_DET', 'thing_NOUN', 'be_VERB', 'the_DET', 'amount_NOUN', 'of_ADP', 'what_PRON', '-PRON-_PRON', 'will_VERB', 'call_VERB', 'life_NOUN', 'which_DET', 'be_VERB', 'require_VERB', 'to_PART', 'be_VERB', 'exchange_VERB', 'for_ADP', '-PRON-_PRON', 'immediately_ADV', 'or_CCONJ', 'in_ADP', 'the_DET', 'long_ADJ', 'run_NOUN']
```
Tokens and Penn tags:

```python
#tokens and penn tags
tagged_string = tag(sample_string,tp = "penn",lemma = False,)
print(tagged_string)
```

```
['the_DT', 'cost_NN', 'of_IN', 'a_DT', 'thing_NN', 'is_VBZ', 'the_DT', 'amount_NN', 'of_IN', 'what_WP', 'i_PRP', 'will_MD', 'call_VB', 'life_NN', 'which_WDT', 'is_VBZ', 'required_VBN', 'to_TO', 'be_VB', 'exchanged_VBN', 'for_IN', 'it_PRP', 'immediately_RB', 'or_CC', 'in_IN', 'the_DT', 'long_JJ', 'run_NN']
```

Tokens and dependency tags:

```python
#tokens and penn tags
tagged_string = tag(sample_string,tp = "dep",lemma = False,)
print(tagged_string)
```
```
['the_det', 'cost_nsubj', 'of_prep', 'a_det', 'thing_pobj', 'is_ROOT', 'the_det', 'amount_attr', 'of_prep', 'what_dobj', 'i_nsubj', 'will_aux', 'call_pcomp', 'life_oprd', 'which_nsubjpass', 'is_auxpass', 'required_relcl', 'to_aux', 'be_auxpass', 'exchanged_xcomp', 'for_prep', 'it_pobj', 'immediately_advmod', 'or_cc', 'in_prep', 'the_det', 'long_amod', 'run_pobj']
```

### Tagging an entire corpus

The function **_tag_corpus()_** takes a directory name as input and returns a list of lists (documents) of lists (tagged tokens). The function uses the **_tag()_** function above (and therefore spaCy) to complete the tagging. The function takes eight arguments (six of which are shared with the **-tag()-** function).
1. **_dirname_** is a string. This should be the name of the folder that your corpus files are in.
2. **_ending_** is a string that indicates the file ending for your corpus files. By default, this is ".txt".
3. **_text_** is a string (e.g., a corpus document). SpaCy places a limit on string size (1,000,000 characters), so you will want to split up any particularly large strings (files).
4. **_tp_** is a string indicating which type of tag to include. Options are universal POS tags "upos", extended Penn POS tags "penn", and universal dependency tags "dep". The default is "upos"
5. **_lemma_** is a Boolean value. If True, the word form will be a lemma. Otherwise, the word form will be a word. The default value is True.
6. **_lower_** is a Boolean value. Lemmas are lower case by default in spaCY. If lemma = False and lower = True, the word form will be a word in lower case. The default value is lower = True
7. **_connect_** is a string. This is the symbol used to connect the word form and the tag. By default, this is an underscore "_"
8. **_ignore_** is a list of universal POS tags to ignore. By default, this list is ["PUNCT","SPACE","SYM"].

```python
def tag_corpus(dirname, ending = ".txt", tp = "upos", lemma = True, lower = True, connect = "_",ignore = ["PUNCT","SPACE"]):
	filenames = glob.glob(dirname + "/*" + ending) #gather all text names
	master_corpus = [] #holder for total corpus

	file_count  = 1 #this is to give the user updates about the pogram's progress
	total = len(filenames) #this is the total number of files to process
	for filename in filenames: #iterate through corpus filenames
		#user message
		print("Tagging " + str(file_count) + " of " + str(total) + " files.")
		file_count += 1 #add one to the file_count

		raw_text = open(filename).read() #open each file
		master_corpus.append(tag(raw_text,tp,lemma,lower,connect,ignore)) #add the tagged text to the master list

	return(master_corpus) #return list
```
Usage example

```python
#tag all files in the "my_corpus" directory using default settings
tagged_corpus = tag_corpus("my_corpus")
```

### Writing tagged corpora to file

If you need to save your tagged corpus (e.g., if it takes a long time for spaCy to process and/or you want to use the corpus in another program such as AntConc), you can use the **_write_corpus()_** function, which writes all of the tokenized texts (including lemmatized or tagged texts) in a corpus to a new directory/folder while retaining the original filenames. The function takes four arguments.
1. **_dirname_** is a string indicating the original folder in which your texts were stored. The original filenames are obtained from this directory.
2. **_new_dirname_** is a string indicating the folder in which you want the tagged files to be written. If the directory doesn't exist, the function will create the new directory.
3. **_corpus_** is a list of lists (corpus documents) of lists (tokens) that will be written to file
4. **_ending_** is a string that indicates what the ending of the original files is. The default value is ".txt"


```python
import os
def write_corpus(dirname,new_dirname,corpus,ending = "txt"):
	dirsep = os.path.sep
	name_list = []
	for x in glob.glob(dirname + "/*" + ending):
		simple_name = x.split(dirsep)[-1] #split the long directory name by the file separator and take the last item (the short filename)
		name_list.append(simple_name)
	if len(name_list) != len(corpus):
		print("Your directory name and your corpus don't match. Please correct this and try again")
		return
	try:
		os.mkdir(new_dirname + "/") #make the new folder
	except FileExistsError: #if folder already exists, then print message
		print("Writing files to existing folder")

	for i, document in enumerate(corpus): #use enumerate to iterate through the corpus list
		new_filename = new_dirname + "/" + name_list[i] #create new filename
		outf = open(new_filename,"w") #create outfile with new filename
		corpus_string = " ".join(document) #turn corpus list into string
		outf.write(corpus_string) #write corpus list
		outf.flush()
		outf.close()
```

```python
#the original corpus is in a folder called "my_corpus", new files will be written to "my_corpus_tagged", and tagged_corpus is the tagged corpus (list of lists of lists)
write_corpus("my_corpus","my_corpus_tagged",tagged_corpus)
```

# Python Exercise 4 (Answers)

Import required modules:

```python
import pickle #load pickle module
import operator #load operator module
import glob #load glob module
```

## Optional, but convenient way to find all punctuation characters:

This is one way to find all of the characters we want to avoid in a corpus. I didn't expect you to write this code (you could accomplish the same thing by looking through the frequency list manually), but you might consider using it in the future.

```python
def corpus_character_freq(dir_name): # I adapted the corpus_freq() function to count characters instead of words
	freq = {} #create an empty dictionary to store the word : frequency pairs

	#create a list that includes all files in the dir_name folder that end in ".txt"
	filenames = glob.glob(dir_name + "/*.txt")

	#iterate through each file:
	for filename in filenames:
		#open the file as a string and lower it
		text = open(filename, errors = "ignore").read().lower()

		#iterate through the characters in the text and add them to the frequency dictionary
		for x in text:
			#the first time we see a particular word we create a key:value pair
			if x not in freq:
				freq[x] = 1
			#when we see a word subsequent times, we add (+=) one to the frequency count
			else:
				freq[x] += 1

	return(freq)

def punct_lister(char_freq_dict):
	punct_list = [] #empty list for punctuation marks
	for x in char_freq_dict: #iterate through keys in the dictionary (i.e., the characters)
		if x not in "abcdefghijklmnopqrstuvwxyz0123456789 ": #if they are not letters, numbers, or spaces
			punct_list.append(x) #add them to the punct_list
	return(punct_list)
```

```python
brown_char_freq = corpus_character_freq("brown_corpus") #frequency dictionary of characters
brown_punct = punct_lister(brown_char_freq)
print(brown_punct)
```

```
['-', ',', '.', "'", '&', '`', '?', '!', ';', ':', '(', ')', '$', '/', '%', '*', '+', '[', ']', '{', '}']
```

## Python Tutorial 4 Exercise
As noted in the tutorial, only a small amount of code has to be changed in order to generate your frequency list. See code below (changes/additions from the tutorial are highlighted in comments).

```python
def tokenize(input_string): #input_string = text string
	tokenized = [] #empty list that will be returned

	##### CHANGES TO CODE HERE #######
	#these are the punctuation marks in the Brown corpus + '"'
	punct_list = ['-',',','.',"'",'&','`','?','!',';',':','(',')','$','/','%','*','+','[',']','{','}','"']

	#this is a sample (but potentially incomplete) list of items to replace with spaces
	replace_list = ["\n","\t"]

	#This is a sample (but potentially incomplete) list if items to ignore
	ignore_list = [""]

	##### CHANGES TO CODE HERE #######
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

def lemmatize(tokenized,lemma_d):
	lemmatized = [] #holder for lemma list

	for word in tokenized: #iterate through words in text
		if word in lemma_d:
			lemmatized.append(lemma_d[word])
		else:
			lemmatized.append(word)
	return(lemmatized)


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

def freq_writer(freq_list,filename):
	outf = open(filename, "w")
	outf.write("word\tfrequency") #write header

	for x in freq_list:
		outf.write("\n" + x[0] + "\t" + str(x[1])) #newline character + word + tab + string version of Frequency
	outf.flush() #flush buffer
	outf.close() #close file

#load lemma dictionary
lemma_dict = pickle.load(open("ant_lemmas.pickle","rb"))

### This is with the BROWN corpus (not required for the Python exercise ###
#create frequency list
brown_freq = corpus_freq("brown_corpus",lemma_dict)

#sort the corpus
sorted_brown = sorted(brown_freq.items(),key=operator.itemgetter(1),reverse = True)

freq_writer(sorted_brown,"brown_freq_clean.txt")
#################################################

### This is with the NICT JLE corpus ############
NICT_freq = corpus_freq("NICT_JLE_Cleaned",lemma_dict)

#sort the corpus
sorted_NICT = sorted(NICT_freq.items(),key=operator.itemgetter(1),reverse = True)

freq_writer(sorted_NICT,"NICT_freq_clean.txt")
```

## Zipped Folder (with results)

For a zipped folder with the above code, the source files, and the output files, [click here]().

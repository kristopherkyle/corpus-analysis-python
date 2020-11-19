# Python Tutorial 9: Calculating and Outputting Text-Level Variables
[Back to Tutorial Index](py_index.md)

(updated 11-19-2020)

In this tutorial, we will apply concepts learned in previous tutorials to create a program that reads in files (e.g., learner corpus texts), calculates a number of indices (i.e., number of words, average frequency score, lexical diversity score) for each text, and then writes the output to a tab-delimited spreadsheet file. This basic program has the building blocks for the creation of much more complex programs (like [TAALED](https://www.linguisticanalysistools.org/taaled.html) and [TAALES](https://www.linguisticanalysistools.org/taales.html)).

We will use a frequency list derived from the Brown Corpus and will process a version of the [NICT JLE learner corpus](https://alaginrc.nict.go.jp/nict_jle/index_E.html). Of course, this code could be used for a wide variety of purposes (and corpus types). [Click here to download version of corpus used in this tutorial.]()

## Import packages and frequency list
First, we will import the packages necessary for subsequent functions:

```python
import math #for logarithmic transformation
import glob #for grabbing filenames
import operator #for dictionary sorting
```

Then, we will import our frequency list using code we generated while completing the exercises from [Python Tutorial 3](Python_Tutorial_3.md):

```python
def splitter(input_string): #presumes that the list is tab-delimitted
	output_list = []
	#insert code here
	for x in input_string.split("\n")[1:]: #iterate through sample string split by "\n", skip header row
		cols = x.split("\t") #split the item by "\t"
		word = cols[0] #the first item will be the word
		freq = cols[1] #the second will be the frequency value
		output_list.append([word,freq]) #append the [word, freq] list to the output list

	return(output_list)

def freq_dicter(input_list):
	output_dict = {}
	#insert code here
	for x in input_list: #iterate through list
		word = x[0] #word is the first item
		freq = float(x[1]) #frequency is second item (convert to float using float())
		output_dict[word] = freq #assign key:value pair

	return(output_dict)

def file_freq_dicter(filename):
	#out_dict = {} #if you use the previously defined function freq_dicter() this is not necessary
	spreadsheet = open(filename).read() #open and read the file here
	split_ss = splitter(spreadsheet)#split the string into rows
	out_dict = freq_dicter(split_ss)#iterate through the rows and assign the word as the key and the frequency as the value

	return(out_dict)
```

Finally, we import our frequency list (see bottom of this tutorial for the code used to create the frequency list). The frequency list can be [downloaded here]().

```python
brown_freq = file_freq_dicter("brown_freq_2020-11-19.txt")
```

## Functions for calculating lexical indices

First, we will use the **_safe_divide()_** function from [Tutorial 3](Python_Tutorial_3.md).

```python
def safe_divide(numerator,denominator): #this function has two arguments
	if denominator == 0: #if the denominator is 0
		output = 0 #the the output is 0
	else: #otherwise
		output = numerator/denominator #the output is the numerator divided by the denominator

	return(output) #return output
```

Then we will create a simple function for calculating the number of words in a text.

```python
def word_counter(low): #list of words
	nwords = len(low)
	return(nwords)
```

Next, we will create a function that will calculate the average (log-transformed) frequency value for the words in each text. This function will look up each word in a text, find the frequency of that word in a reference corpus, log-transform the frequency value (to help account for the Zipfian distribution of words in a corpus), and create an averaged score for the whole text.

```python
def frequency_count(tok_text,freq_dict):
	freq_sum = 0
	word_sum = 0
	for x in tok_text:
		if x in freq_dict: #if the word is in the frequency dictionary
			freq_sum += math.log(freq_dict[x]) #add the (logged) frequency value to the freq_sum counter
			word_sum += 1 #add one to the word_sum counter
		else:
			continue #if the word isn't in the frequency dictionary, we will ignore it in our index calculation

	return(safe_divide(freq_sum,word_sum)) #return average (logged) frequency score for words in the text
```

Finally (for now), we will create a function that calculates a score representing the diversity of lexical items in a text. This particular index, moving average type-token ratio (MATTR) has been shown to be independent of text length (unlike many other well-known indices). See Covington et al. (2010), Kyle et al. (2020), and/or Zenker and Kyle (2020) for more details.

```python
def lexical_diversity(tok_text,window_length = 50): #this is for moving average type token ratio (TTR). See Covington et al., 2010; Kyle et al. (2020); Zenker & Kyle (2020)
	if len(tok_text) < (window_length + 1):
		ma_ttr = safe_divide(len(set(tok_text)),len(tok_text))

	else:
		sum_ttr = 0
		denom = 0
		for x in range(len(tok_text)):
			small_text = tok_text[x:(x + window_length)]
			if len(small_text) < window_length:
				break
			denom += 1
			sum_ttr+= safe_divide(len(set(small_text)),float(window_length))
		ma_ttr = safe_divide(sum_ttr,denom)

	return ma_ttr
```

## Tokenizer
We will use a version of the **_tokenize()_** function from [Tutorial 4](Python_Tutorial_4.md) to tokenize our texts.

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
```

## Putting it all together
Now, we can create a function **_text_processor()_** that will read all files in a folder, calculate a number of lexical indices, and then outputs those to a tab-delimited file.

```python
def text_processor(folder,outname): #folder name, name of output file
	corp_dict = {} #dictionary to store all data (not absolutely necessary, but potentially helpful)
	outf = open(outname,"w") #create output file
	outf.write("\t".join(["filename","nwords","av_freq","mattr"])) #write header
	filenames = glob.glob(folder + "/*") #get filenames in folder

	for filename in filenames: #iterate through filenames
		print(filename)
		text_d = {} #create text dictionary to store indices for each text
		simple_fname = filename.split("/")[-1] #get last part of filename
		text = tokenize(open(filename, errors = "ignore").read()) #read file and tokenize it

		#add data to the text dictionary:
		text_d["filename"] = simple_fname
		text_d["nwords"] = word_counter(text) #calculate number of words
		text_d["av_freq"] = frequency_count(text,brown_freq) #calculate average frequency
		text_d["mattr"] = lexical_diversity(text)

		### add more stuff to dictionary here as needed ###

		#add text dictionary to corpus dictionary (not absolutely necessary, but potentially helpful)
		corp_dict[simple_fname] = text_d

		out_line = [text_d["filename"],str(text_d["nwords"]),str(text_d["av_freq"]),str(text_d["mattr"])] #create line for output, make sure to turn any numbers to strings
		outf.write("\n" + "\t".join(out_line)) #write line

	outf.flush() #flush buffer
	outf.close() #close_file

	return(corp_dict)
```

Below, we use our **_text_processor()_** function to calculate lexical indices in the NICT JLE learner corpus (though almost any properly-formatted corpus could be used!)

```python
nict_data = text_processor("NICT_JLE_CLEANED","lex_richness_JLE.txt") #write data to a file named "lex_richness_JLE.txt"

print(nict_data["file00301.txt"]) #print the data for one file
```

```
{'filename': 'file00301.txt', 'nwords': 1109, 'av_freq': 7.110700325247902, 'mattr': 0.7109433962264144}
```

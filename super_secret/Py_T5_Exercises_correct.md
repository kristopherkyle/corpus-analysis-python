# Python Exercise 5 (Answers)

## Import required modules:
```python
import glob
import re
import random
random.seed(1) #set seed
```

## Necessary Functions from tutorial:
```python
## Define Functions:

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

def concord(tok_list,target,nleft,nright):
	hits = [] #empty list for search hits

	for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
		if x in target: #if the item matches one of the target items

			if idx < nleft: #deal with left context if search term comes early in a text
				left = tok_list[:idx] #get x number of words before the current one (based on nleft)
			else:
				left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)

			t = x #set t as the item
			right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
			hits.append([left,t,right]) #append a list consisting of a list of left words, the target word, and a list of right words

	return(hits)

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

def concord_regex(tok_list,target_regex,nleft,nright):
	hits = [] #empty list for search hits

	for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
		if re.compile(target_regex).match(x) != None: #If the target regular expression finds a match in the string (the slightly strange syntax here literally means "if it doesn't not find a match")

			if idx < nleft: #deal with left context if search term comes early in a text
				left = tok_list[:idx] #get x number of words before the current one (based on nleft)
			else:
				left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)

			t = x #set t as the item
			right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
			hits.append([left,t,right]) #append a list consisting of a list of left words, the target word, and a list of right words

	return(hits)

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

#From Tutorial 4:
def freq_simple(tok_list):
	#first we define an empty dictionary
	freq = {}

	#then we iterate through our list
	for x in tok_list:
		#the first time we see a particular word we create a key:value pair
		if x not in freq:
			freq[x] = 1
		#when we see a word subsequent times, we add (+=) one to the frequency count
		else:
			freq[x] += 1
	#finally, we return the frequency dictionary
	return(freq)
```


## Code to Complete Exercises:

Note that a zipped folder with the code, the source files, and the output files for these exercises are [available click here](https://github.com/kristopherkyle/corpus-analysis-python/raw/master/super_secret/Py_T5_Exercises_correct.zip).

**1. Create a sample of 50 concordance lines of the word “record” in the Brown corpus. Use ten words of right context and ten words of left context. Write the concordance lines to a file called “1_record.txt”. Then, read the concordance lines and identify at least two senses of the word “record”. Be sure to provide at least two examples of each sense. Report your findings in your .py file (use hashtags at the beginning of each line)**

```python
#create concordance lines:
record_conc_50 = corp_conc("brown_corpus",["record"],50,10,10)
#write them to a file:
write_concord("1_record.txt",record_conc_50)
#record as a noun - the best result ever witnessed for a particular competition
#record as a verb - store things (such as pictures) for later use (ish)
```

**2. Update the corp_conc() function in a manner that allows you to use the concord_regex() function instead of the concord() function and call it corp_conc_regex(). Then, create a sample of 50 concordance lines with node/target words that start with “repe”. Write the concordance lines to a file called “2repe.txt”(What is the most common root word in your sample?**

See comments in corp_conc_regex() function below. Minimal changes are needed to convert corp_conc() into corp_conc_regex().

```python
#NOTE: This is the corp_conc() function with TWO changes. 1. The name is changed. 2. It uses the concord_regex() function instead of the concord() function.
#NO OTHER CHANGES ARE NECESSARY!
def corp_conc_regex(corp_folder,target,nhits,nleft,nright):
	hits = []

	filenames = glob.glob(corp_folder + "/*.txt") #make a list of all .txt file in corp_folder
	for filename in filenames: #iterate through filename
		text = tokenize(open(filename).read())
		#add concordance hits for each text to corpus-level list:
		for x in concord_regex(text,target,nleft,nright): #here we use the concord() function to generate concordance lines
			hits.append(x)

	# now we generate the random sample
	if len(hits) <= nhits: #if the number of search hits are less than or equal to the requested sample:
		print("Search returned " + str(len(hits)) + " hits.\n Returning all " + str(len(hits)) + " hits")
		return(hits) #return entire hit list
	else:
		print("Search returned " + str(len(hits)) + " hits.\n Returning a random sample of " + str(nhits) + " hits")
		return(random.sample(hits,nhits)) #return the random sample
```

Them, we can complete the task:

```python
#create concordance lines:
repe_conc_50 = corp_conc_regex("brown_corpus","repe.*",50,10,10)

#write them to a file:
write_concord("2_repe.txt",repe_conc_50)

#sort the lines by node word:
repe_conc_50_sorted = sorted(repe_conc_50,key = lambda x: x[1])

#we can print these and count manually to see which is the most common
for x in repe_conc_50_sorted:
	print(x)

#OR we can create a list of node words and use our freq_simple() function from tutorial 4:
repe_hits = [] #empty list to fill
for x in repe_conc_50: #iterate through concordance lines
	repe_hits.append(x[1]) #add node word (x[1]) to list

#I added freq_simple() from Python Tutorial 4 to the defined function list
repe_freq = freq_simple(repe_hits)
print(repe_freq) #the most frequent hit was "repeated"
```

```
{'repeat': 10, 'repel': 4, 'repeated': 15, 'repetition': 5, 'repelled': 3, 'repetitive': 1, 'repeater': 1, 'repertoire': 1, 'repeal': 1, 'repeatedly': 5, 'repertory': 2, 'repeats': 1, 'repeating': 1}
```


**3. Create a sample of 50 concordance lines that include words with the nominalized suffix “ation” (be sure to include plural forms). Bonus points if you are able to avoid words such as “nation” (which is not a transparent nominalization-don’t overthink this). Write your results to a file called “3_ation.txt”**


```python
#create concordance lines:
ation_conc_50 = corp_conc_regex("brown_corpus",".*ation.*",50,10,10) #this is the basic answer to the question
#write them to a file:
write_concord("3_ation.txt",ation_conc_50)
```

**For Bonus points (using a more advanced regular expression):**

```python
#create concordance lines:
#".*[aeiou].ation.*" means: any combination of letters (".*") followed by one instance of a vowel ("[aeiou]"),any other character (".") followed by "ation" followed by anything else (".*")
ation_conc_50_bonus = corp_conc_regex("brown_corpus",".*[aeiou].ation.*",50,10,10) #this uses a more complex regular expression (it probably still isn't perfect).
#write them to a file:
write_concord("3_ation_bonus.txt",ation_conc_50_bonus)
```

**4. Create a version of the “write_concord()” function that places a tab character between items in the context lists instead of a space. Do a concordance search of your choosing (in Brown or another corpus) and write the concordance lines to a file called “4_my_search.txt”**

See write_concord_tab() code below. For this version we only have to change the two ".join()" commands slightly. For now, we can ignore the header (which will be off).

```python

def write_concord_tab(outname, conc_list):
	outf = open(outname,"w")
	outf.write("left_context\tnode_word\tright_context") #write header (optional)
	for x in conc_list:
		left = "\t".join(x[0]) #join the left context list into a string using spaces
		target = x[1] #this is the node/target word
		right = "\t".join(x[2]) #join the left context list into a string using spaces
		outf.write("\n" + left + "\t" + target + "\t" + right)
	outf.flush()
	outf.close()

```

Once we have our new version of the write_concord() function, we can complete our task:

```python
#create concordance lines:
climb_conc_50 = corp_conc_regex("brown_corpus","climb.*",50,10,10) #search for forms of the word "climb"
#write them to a file:
write_concord_tab('4_my_search.txt',climb_conc_50)
```

# Python Exercise 6 (Answers)

## Necessary Functions from tutorial:
First, we will define all required functions from the tutorial:

```python
#import required packages
import re
import glob
import operator
import math

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

#here we use a version of the freq_simple() function that updates a pre-existing dictionary instead of returning a new dictionary
def freq_update(tok_list,freq_dict): #this takes a list (tok_list) and a dictionary (freq_dict) as arguments
	for x in tok_list: #for x in list
		if x not in freq_dict: #if x not in dictionary
			freq_dict[x] = 1 #create new entry
		else: #else: add one to entry
			freq_dict[x] += 1



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

## My answers to the exercises:


**1. Using the words investigation and investigations as the search term, identify the most strongly associated collocates that occur immediately before the search term with regard to MI and T score (i.e., your left context should be set to one and your right context should be set to 0). Choose one of the items from each of your collocate lists and hypothesize about the nature of the relationship between the collocate and the target word. Is the relationship grammatical? idiomatic? something else?**

```python
investigation_l1r0 = soa(corpus_context_freq("brown_corpus","investigation.*",1,0))
head(investigation_l1r0["mi"])
```

```
an      4.696282111104258
of      2.068137680000618
the     0.4737178589428962
```

**2. Now do the same thing, but set your collocate search to include only the word immediately following the search term.**

```python
investigation_l0r1 = soa(corpus_context_freq("brown_corpus","investigation.*",0,1))
head(investigation_l0r1["mi"])
```

```
of      2.7786310628056334
```

**3. Pick a search term and corpus of your choosing. You are welcome to use the Brown corpus, but you are also welcome to use some other corpus. Determine the most strongly associated items with your search term based on two statistics of your choosing. Use two span settings (left and right should both be no more than ten and no less than two), and compare your results. What specific effects does search span seem to have on your findings?**

Span setting 1 (3L and 3R):

```python
climbing_r3l3 = soa(corpus_context_freq("brown_corpus","climb.*",3,3))
head(climbing_r3l3["mi"])
```

```
steps   9.553338881748731
back    6.2692428603871075
into    5.3785726172369195
up      5.300951720114446
on      3.951802156492059
his     3.89823449247147
he      3.8121362946960544
and     3.6317229341543933
to      3.358154527394878
the     3.194989409217068
in      2.6517789864465806
a       2.354656548988197
of      1.5184227010506028
```

Span setting 2: (10L and 10R):

```python
climbing_r10l10 = soa(corpus_context_freq("brown_corpus","climb.*",10,10))
head(climbing_r10l10["mi"])
```

```
steps   10.138301382469887
down    6.642412772905056
back    6.2692428603871075
up      6.148948626669396
into    6.056644522349558
would   5.778917233804027
he      5.686605412612195
they    5.500851781002248
her     5.465163070362364
there   5.449566215311346
about   5.359368406339768
she     5.188749634727371
out     5.1510110931262885
his     5.090879570413866
who     5.048131127142652
to      4.773192026673722
on      4.7294097351556115
the     4.722920964901845
and     4.690616623207962
was     4.602421591981985
```

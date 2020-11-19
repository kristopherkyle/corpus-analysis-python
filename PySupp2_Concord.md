# Advanced Concordancing
[Back to Tutorial Index](py_index.md)

(updated 11-19-2020)

This supplemental code shows one way to conduct concordance searches in more complex situations (e.g., when the target items are n-grams and/or when you want to search for a target item + an item in the context).

### Preliminaries
First, we will import necessary packages and define a tokenization function (note that this will likely need to be refined for one's particular purposes).

```python
import glob
import re
import random

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
```

## Advanced concordancing
As alluded to above, the **_concord2()_** function will allow for more complex concordance searches. Target items can be words, n-grams, or a mixture of the two. Searches can also be restricted with regard to particular items (in this case words) in the context.

The **_concord2()_** function takes the following arguments:
- **_tok_list_** a tokenized list of strings
- **_target_** a list of the target strings (e.g., words and/or n-grams)
- **_nleft_** length of preceding context (in number of words)
- **_nright_** length of following context (in number of words)
- **_cntxt_search_** a list of the target strings (e.g., words to search for in the context)

```python
def concord2(tok_list,target,nleft,nright,cntxt_search = None): #target is list of target items, cntxt_search is list of items to search for in context.
	hits = [] #empty list for search hits

	for idx, x in enumerate(tok_list): #iterate through token list using the enumerate function. idx = list index, x = list item
		hit = False #Boolean value to check for hits
		ngram = False #whether target item is an ngram
		for y in target: #iterate through target items
			if len(y.split(" ")) == 1: #if the target item is a word
				if x == y: #if the word is a match with the target item
					hit = True
					break #if we have a hit move on to concordance lines
			else:
				gram_size = len(y.split(" ")) #length of n-gram
				x_ngram = " ".join(tok_list[idx:idx+gram_size]) #make string version of current ngram frame
				if x_ngram == y: #check to see if current nogram matches target ngram
					hit = True
					x = x_ngram #change current item to ngram
					ngram = True
					break #if we have a hit move on to concordance lines

		if hit == True: #if the item matches one of the target items

			if idx < nleft: #deal with left context if search term comes early in a text
				left = tok_list[:idx] #get x number of words before the current one (based on nleft)
			else:
				left = tok_list[idx-nleft:idx] #get x number of words before the current one (based on nleft)

			t = x #set t as the item
			if ngram == False:
				right = tok_list[idx+1:idx+nright+1] #get x number of words after the current one (based on nright)
			else:
				right = tok_list[idx+1+gram_size:idx+gram_size+nright+1]

			if cntxt_search == None:
				hits.append([left,t,right]) #append a list consisting of a list of left words, the target word, and a list of right words
			else:
				cntxt_hit = False
				for item in right + left:
					if item in cntxt_search:
						cntxt_hit = True
						break
				if cntxt_hit == True:
					hits.append([left,t,right]) #append a list consisting of a list of left words, the target word, and a list of right words

	return(hits)
```

Now we can use the function to get concordance lines for n-grams:
```python
sample = "I like to eat healthy food. On the other hand, I also really like pizza. But to be precise, on the other hand, I like pepperoni pizza in my hand (right before it goes in my mouth)."

for x in concord2(tokenize(sample),["other hand"], 5,5):
	print(x)
```
```
[['healthy', 'food', '.', 'on', 'the'], 'other hand', ['i', 'also', 'really', 'like', 'pizza']]
[['be', 'precise', ',', 'on', 'the'], 'other hand', ['i', 'like', 'pepperoni', 'pizza', 'in']]
```
And, we can constrain our searches so that they only include hits with particular words in the context:
```python
for x in concord2(tokenize(sample),["other hand"], 5,5, cntxt_search = ["precise"]):
	print(x)
```
```
[['be', 'precise', ',', 'on', 'the'], 'other hand', ['i', 'like', 'pepperoni', 'pizza', 'in']]
```
Now, we can update our corpus concordance function to include our **_concord2()_** function.

The **_corp_conc2()_** function takes the following arguments:
- **_corp_folder_** name of folder that includes the corpus files (this should be in your working directory!)
- **_target_** a list of the target strings (e.g., words and/or n-grams)
- **_nleft_** length of preceding context (in number of words)
- **_nright_** length of following context (in number of words)
- **_cntxt_search_** a list of the target strings (e.g., words to search for in the context)

```python
def corp_conc2(corp_folder,target,nhits,nleft,nright,cntxt_search = None): #cntxt_search is list of items to search for in context
	hits = []

	filenames = glob.glob(corp_folder + "/*.txt") #make a list of all .txt file in corp_folder
	for filename in filenames: #iterate through filename
		text = tokenize(open(filename).read())
		#add concordance hits for each text to corpus-level list:
		for x in concord2(text,target,nleft,nright,cntxt_search): #here we use the concord() function to generate concordance lines
			hits.append(x)

	# now we generate the random sample
	if len(hits) <= nhits: #if the number of search hits are less than or equal to the requested sample:
		print("Search returned " + str(len(hits)) + " hits.\n Returning all " + str(len(hits)) + " hits")
		return(hits) #return entire hit list
	else:
		print("Search returned " + str(len(hits)) + " hits.\n Returning a random sample of " + str(nhits) + " hits")
		return(random.sample(hits,nhits)) #return the random sample
```
We can now test our function using the Brown corpus and an n-gram search (this presumes that you have the Brown corpus in your working directory):
```python
brown_otoh = corp_conc2("brown_corpus",["on the other hand"],25,5,5)
for x in brown_otoh:
	print(x)
```
```
Search returned 58 hits.
 Returning a random sample of 25 hits
[['it', 'time', 'and', 'again', '.'], 'on the other hand', ['the', 'women', 'class', 'members', 'appeared']]
[['signal', 'ambiguity', 'or', 'uncertainty', '.'], 'on the other hand', ['facts', 'may', 'be', 'concealed', '--']]
[['.', 'sex', 'was', 'both', '.'], 'on the other hand', ['some', 'unwed', 'mothers', 'had', 'had']]
[['to', 'achieve', 'those', 'goals', '.'], 'on the other hand', ['it', 'is', 'no', 'interference', 'with']]
[['astwood', ',', '1954', ')', '.'], 'on the other hand', ['there', 'are', 'a', 'few', 'antithyroid']]
[['well', 'developed', 'respiratory', 'bronchioles', ','], 'on the other hand', ['appear', 'to', 'be', 'the', 'only']]
[['a', 'busted', 'front', 'spring', '.'], 'on the other hand', ['howsomever', ',', 'maybe', 'you', 'wouldn']]
[['setback', 'to', 'the', 'constitution', '.'], 'on the other hand', ['molesworth', 'was', 'naturally', 'assailed', 'in']]
[['individual', 'objects', '.', 'if', ','], 'on the other hand', ['they', 'opted', 'for', 'representation', ',']]
[['original', 'cession', 'was', 'invalid', '.'], 'on the other hand', ['he', 'did', 'not', 'want', 'to']]
[['real', 'headaches', 'in', 'store', '.'], 'on the other hand', ['the', 'process', 'of', 'obsoleting', 'an']]
[[',', 'dolores', 'would', 'crack', '.'], 'on the other hand', ['if', 'she', 'didn', "'t", 'remove']]
[[',', 'bestial', 'and', 'unworthy', '.'], 'on the other hand', ['wifely', 'supremacy', 'demeans', 'the', 'husband']]
[['happier', 'one', '.', 'research', ','], 'on the other hand', ['has', 'shown', 'many', 'stepmothers', 'to']]
[['be', 'moot', '.', 'if', ','], 'on the other hand', ['it', 'is', 'not', 'settled', ',']]
[['of', 'which', 'it', 'arises', '.'], 'on the other hand', ['we', 'cannot', 'regard', 'artistic', 'invention']]
[['newport', ',', 'and', 'providence', '.'], 'on the other hand', ['dr', '.', 'ezra', 'styles', 'recorded']]
[['not', 'seem', 'very', 'bright', '.'], 'on the other hand', ['to', 'greet', 'them', 'with', 'delight']]
[['cause', 'increased', 'convulsive', 'discharges', '.'], 'on the other hand', ['the', 'temporary', 'reduction', 'in', 'hypothalamic']]
[['that', 'enacted', 'for', '1960', '.'], 'on the other hand', ['the', 'new', 'authority', 'of', '$3']]
[[';', ';', 'while', 'jones', ','], 'on the other hand', ['appeared', 'perfectly', 'confident', 'and', 'ulyate']]
[['heads', 'and', 'two', 'tails', '.'], 'on the other hand', ['they', ',', 'or', 'it', ',']]
[['of', 'time', 'and', 'change', '.'], 'on the other hand', ['christian', 'faith', 'knows', 'that', 'death']]
[['to', 'himself', '.', 'or', ','], 'on the other hand', ['are', 'unlikely', 'facts', 'being', 'stated']]
[['face-to-face', 'group', 'of', 'individuals', '.'], 'on the other hand', ['many', 'a', 'pastor', 'is', 'so']]
```
We can also test our function with a constrained context:
```python
brown_otoh_modal = corp_conc2("brown_corpus",["on the other hand"],25,5,5,cntxt_search = ["may","would","could","might"])

for x in brown_otoh_modal:
	print(x)
```
```
Search returned 5 hits.
 Returning all 5 hits
[['signal', 'ambiguity', 'or', 'uncertainty', '.'], 'on the other hand', ['facts', 'may', 'be', 'concealed', '--']]
[['would', 'be', 'no', 'epidemic', '.'], 'on the other hand', ['a', 'similar', 'attack', 'might', 'have']]
[['your', 'hands', '--', 'now', '.'], 'on the other hand', ['you', 'may', 'seek', 'his', 'favor']]
[['like', '.', 'his', 'election', ','], 'on the other hand', ['would', 'unquestionably', 'strengthen', 'the', '``']]
[[',', 'dolores', 'would', 'crack', '.'], 'on the other hand', ['if', 'she', 'didn', "'t", 'remove']]
```

# Python Tutorial 6: Keyness and Collocation
[Back to Tutorial Index](py_index.md)

### Keyness
In corpus linguistics, a linguistic item (e.g., a word) is "key" when it occurs more frequently in one corpus than another. There are multiple methods of calculating keyness (for a nice overview of these, see Gabrielatos, 2018).

In order to calculate keyness, we need frequency information from two corpora (referred to here as a target corpus and a reference corpus). The function **_keyness()_** below takes three arguments and returns a dictionary consisting of {word : keyness_value} key : value pairs. This function calculates three types of effect sizes for keyness, but pointedly does not calculate statistical significance (which is skewed by the size of the corpora - see Gabrielatos, 2018).
1. **_freq_dict1_** is a dictionary consisting of {word : raw_frequency} values for the target corpus. Because some methods of calculating keyness require raw frequency counts, the dictionary must include raw counts.
2. **_freq_dict2_** is a dictionary consisting of {word : raw_frequency} values for the reference corpus. Because some methods of calculating keyness require raw frequency counts, the dictionary must include raw counts.
3. **_effect_** is a string indicating which keyness method to use. Options include "log-ratio", "%diff", and "odds-ratio". See Gabrielatos (2018) for more details.

```python
import math
def keyness(freq_dict1,freq_dict2,effect = "log-ratio"): #this assumes that raw frequencies were used. effect options = "log-ratio", "%diff", "odds-ratio"
	keyness_dict = {}
	ref_dict = {}

	size1 = sum(freq_dict1.values())
	size2 = sum(freq_dict2.values())

	def log_ratio(freq1,size1,freq2,size2): #presumes that the frequencies are normed
		freq1_norm = freq1/size1 * 1000000
		freq2_norm = freq2/size2 * 1000000
		index = math.log2(freq1/freq2)
		return(index)

	def perc_diff(freq1,size1,freq2,size2):
		freq1_norm = freq1/size1 * 1000000
		freq2_norm = freq2/size2 * 1000000
		index = ((freq1_norm-freq2_norm)  * 100)/freq2_norm
		return(index)

	def odds_ratio(freq1,size1,freq2,size2):
		if size1 - freq1 == 0: #this will be a very rare case, but would kill program
			size1 += 1
		if size2 - freq2 == 0: #this will be a very rare case, but would kill program
			size2 += 1
		index = (freq1/(size1-freq1))/(freq2/(size2-freq2))
		return(index)


	#create combined word list (we will actually use a dictionary for speed)
	for x in freq_dict1:
		if x not in ref_dict:
			ref_dict[x] = 0 #the zero isn't used for anything
	for x in freq_dict2:
		if x not in ref_dict:
			ref_dict[x] = 0 #the zero isn't used for anything

	#if our item doesn't occur in one of our reference corpora, we need to make an adjustment
	#here, we change the frequency to a very small number (.00000001) instead of zero
	#this is because zeros will cause problems in our calculation of keyness
	for item in ref_dict:
		if item not in freq_dict1 or freq_dict1[item] == 0:
			freq_dict1[item] = .00000001 #tiny number
		if item not in freq_dict2 or freq_dict2[item] == 0:
			freq_dict2[item] = .00000001 #tiny number

		if effect == 'log-ratio':
			print("OK")
			keyness_dict[item] = log_ratio(freq_dict1[item],size1,freq_dict2[item],size2)

		elif effect == "%diff":
			keyness_dict[item] = perc_diff(freq_dict1[item],size1,freq_dict2[item],size2)

		elif effect == "odds-ratio":
			keyness_dict[item] = odds_ratio(freq_dict1[item],size1,freq_dict2[item],size2)

	return(keyness_dict)
```
Usage examples:

```python
#using the default log ratio method of calculating of keyness
keyness_dict_lr = keyness(target_freq,reference_freq)

#using the percent difference method of calculating of keyness
keyness_dict_diff = keyness(target_freq,reference_freq,effect = "%diff")

#using the odds ratio method of calculating of keyness
keyness_dict_or = keyness(target_freq,reference_freq, effect = "odds-ratio")

```


### Collocation
Another common analysis in corpus linguistics is to determine the strength of association between words that occur together. Collocation analyses highlight words that occur together with an unexpected frequency. The most common methods of calculating the strength of association between linguistic items are pointwise mutual information (MI) and T-score (T), though there are many other methods that may be more appropriate depending on the analysis (see, e.g., Gries & Ellis, 2015).

The **_collocator()_** function below calculates a number of collocation statistics. It takes six arguments and returns a dictionary consisting of {word : collocation} key : value pairs. Note that the function uses the **_corpus_frequency()_** function, which is described in Python Tutorial 5.
1. **_corpus_list_** is a tokenized corpus list (list of lists of lists).
2. **_target_** is a string that should consist of the word for which you want to find collocates
3. **_left_** is an integer that indicates how far to the left of the node/target word you want to search. By default, the left span is 4.
4. **_right_** is an integer that indicates how far to the right of the node/target word you want to search. By default, the right span is 4.
5. **_stat_** is a string that indicates the association strength calculation method. Choices include "MI" and "T". By default, this value is set to "MI"
6. **_cutoff_** is an integer that indicates the minimum frequency threshold for the collocation analysis. If a word occurs with the target/node word with a frequency below the cutoff, it will be ignored. The default cutoff value is 5.


```python
def collocator(corpus_list,target, left = 4,right = 4, stat = "MI", cutoff = 5): #returns a dictionary of collocation values
	corp_freq = corpus_frequency(corpus_list) #use the corpus_frequency function to create frequency list
	nwords = sum(corp_freq.values()) #get corpus size for statistical calculations
	collocate_freq = {} #empty dictionary for storing collocation frequencies
	r_freq = {} #for hits to the right
	l_freq = {}  #for hits to the left
	stat_dict = {} #for storing the values for whichever stat was used

	def freq(l,d): #this takes a list (l) and a dictionary (d) as arguments
		for x in l: #for x in list
			if x not in d: #if x not in dictionary
				d[x] = 1 #create new entry
			else: #else: add one to entry
				d[x] += 1

	#begin collocation frequency analysis
	for text in corpus_list:
		if target not in text: #if target not in the text, don't search it for other words
			continue
		else:
			last_index = len(text) -1 #get last index number
			for i , word in enumerate(text):
				if word == target:
					start = i-left #beginning of left span
					end = i + right + 1 #end of right span. Note, we have to add 1 because of the way that slices work in python
					if start < 0: #if the left span goes beyond the text
						start = 0 #start at the first word
					#words to the right
					lspan_list = text[start:i] #for counting words on right
					freq(lspan_list,l_freq) #update l_freq dictionary
					freq(lspan_list,collocate_freq) #update collocate_freq dictionary

					rspan_list = text[i+1:end] #for counting words on left. Note, have to add +1 to ignore node word
					freq(rspan_list,r_freq) #update r_freq dictionary
					freq(rspan_list,collocate_freq) #update collocate_freq dictionary

	#begin collocation stat calculation

	for x in collocate_freq:
		observed = collocate_freq[x]
		if observed < cutoff: #if the collocate frequency doesn't meet the cutoff, ignore it
			continue
		else:
			expected = (corp_freq[target] * corp_freq[x])/nwords #expected = (frequency of target word (in entire corpus) * frequency of collocate (in entire corpus)) / number of words in corpus
			if stat == "MI": #pointwise mutual information
				mi_score = math.log2(observed/expected) #log base 2 of observed co-occurence/expected co-occurence
				stat_dict[x] = mi_score
			elif stat == "T": #t-score
				t_score = math.log2((observed - expected)/math.sqrt(expected))
				stat_dict[x] = t_score
			elif stat == "freq":
				stat_dict[x] = collocate_freq[x]
			elif stat == "right": #right frequency
				stat_dict[x] = r_freq[x]
			elif stat == "left":
				stat_dict[x] = l_freq[x]

	return(stat_dict) #return stat dict
```
Usage examples

```python
#calculate collocation strength using default settings
collocation_dict = collocator(tokenized_corpus,"run")

#calculate collocation with T score instead of MI
collocation_dict = collocator(tokenized_corpus,"run", stat = "T")

#calculate collocation with custom span
collocation_dict = collocator(tokenized_corpus,"run", left = 5, right = 6)

```

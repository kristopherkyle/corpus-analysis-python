The function **_load_lemma_** takes a single argument and returns a dictionary consisting of {"word" : "lemma"} pairs.
1. **_lemma_file_** is a string. It should be the name of your lemma list (don't forget place this file in the same folder as your Python script and set your working directory!)

```python
def load_lemma(lemma_file): #this is how we load a lemma_list
	lemma_dict = {} #empty dictionary for {token : lemma} key : value pairs
	lemma_list = open(lemma_file).read() #open lemma_list
	lemma_list = lemma_list.replace("\t->","") #replace marker, if it exists
	lemma_list = lemma_list.split("\n") #split on newline characters
	for line in lemma_list: #iterate through each line
		tokens = line.split("\t") #split each line into tokens
		if len(tokens) <= 2: #if there are only two items in the token list, skip the item (this fixed some problems with the antconc list)
			continue
		lemma = tokens[0] #the lemma is the first item on the list
		for token in tokens[1:]: #iterate through every token, starting with the second one
			if token in lemma_dict:#if the token has already been assigned a lemma - this solved some problems in the antconc list
				continue
			else:
				lemma_dict[token] = lemma #make the key the word, and the lemma the value

	return(lemma_dict)
```

The example below uses [Laurence Anthony's lemma list](https://www.laurenceanthony.net/resources/wordlists/antbnc_lemmas_ver_003.zip), which includes lemmas for all words that occur at least twice in the BNC.

```python
lemma_dict = load_lemma("antbnc_lemmas_ver_003.txt")
```

# Python Tutorial 3 Exercises
 Imagine that you have a spreadsheet consisting of words, their corpus frequency, and their corpus range (i.e., the number of corpus documents in which they occur). Your goal is to write a script that opens the spreadsheet and converts the data to a dictionary format which can be used for downstream processes. The following exercises will build towards that goal.

## 1) Create an empty dictionary called "d1". Then, using indexing, create a key : value pair in "d1" where the word in the sample list ("l1" in the code below) is the key and the number (in this case, a frequency value) is the key.

```python
l1 = ['the', '5226263'] #frequency of the word "the" in the British National Corpus (BNC)

#define empty dictionary "d1" here
d1 = {}
#assign the key : value pair here
d1[l1[0]] = l1[1]
#if you completed the exercise correctly, the following code will result in the output below
print(d1["the"])
```

```
5226263
```

## 2) Write a function named "splitter()" that takes a string (in the format below) and converts it into a list of lists. The outer list should be split by newline characters ("\n") (i.e., will indicate rows), and the inner list should be split by tabs ("\t") (i.e., will indicate columns). Your function should return the list of lists.


Note, these are raw frequency scores for the written section of the British National Corpus (90 million words)

```python
sample_string = "the\t5226263\nof\t2691108\nand\t2215331\nto\t2189223\na\t1827567\nin\t1677334"

#this is an outline for your function:
def splitter(input_string):
	output_list = []
	#insert code here
	for x in input_string.split("\n"): #iterate through sample string split by "\n"
		cols = x.split("\t") #split the item by "\t"
		word = cols[0] #the first item will be the word
		freq = cols[1] #the second will be the frequency value
		output_list.append([word,freq]) #append the [word, freq] list to the output list

	return(output_list)
```

After completing your function, you should be able to run the following code and get the results below

```python
sample_list = splitter(sample_string)
print(sample_list)
```

```
[['the', '5226263'], ['of', '2691108'], ['and', '2215331'], ['to', '2189223'], ['a', '1827567'], ['in', '1677334']]
```

## 3) Now write a function called "freq_dicter()" that takes the output of the splitter() function as an argument and returns a dictionary in the following format: {'word' : frequency}. Be sure to convert the frequency value into a float.

```python
sample_list = [['the', '5226263'], ['of', '2691108'], ['and', '2215331'], ['to', '2189223'], ['a', '1827567'], ['in', '1677334']]

#this is an outline for your function:
def freq_dicter(input_list):
	output_dict = {}
	#insert code here
	for x in input_list: #iterate through list
		word = x[0] #word is the first item
		freq = float(x[1]) #frequency is second item (convert to float using float())
		output_dict[word] = freq #assign key:value pair

	return(output_dict)
```

After completing your function, you should be able to run the following code and get the results below

```python
sample_dict = freq_dicter(sample_list)
print(sample_dict)
```

```
{'the': 5226263.0, 'of': 2691108.0, 'and': 2215331.0, 'to': 2189223.0, 'a': 1827567.0, 'in': 1677334.0}
```
## 4) Now, write a function called "file_freq_dicter()" that takes a filename as an argument and subsequently reads the file (which is expected to be in tab-delimited format consisting of words and their frequencies) and outputs a dictionary consisting of word : frequency pairs. Be sure that frequency figures are converted from strings to floats. Then, use your function to open the file bnc_written_freq.txt and convert it to a dictionary. Don't forget to place the file in the same folder as your script (and set your working directory!)

```python
def file_freq_dicter(filename):
	#out_dict = {} #if you use the previously defined function freq_dicter() this is not necessary
	spreadsheet = open(filename).read() #open and read the file here
	split_ss = splitter(spreadsheet)#split the string into rows
	out_dict = freq_dicter(split_ss)#iterate through the rows and assign the word as the key and the frequency as the value

	return(out_dict)
```

If your function works properly, the following code should result in the output below.

```python
bnc_freq = file_freq_dicter("bnc_written_freq.txt")
print(bnc_freq["hearing"])
print(bnc_freq["python"])
```

```
4527.0
109.0
```

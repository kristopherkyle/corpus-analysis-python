[Back to Tutorial Index](py_index.md)
Updated 9-22-2020
 
# Python Tutorial 3

### Dictionaries, Tuples, Functions, and Files

## Part I: Dictionaries

Dictionaries are storage and retrieval objects (like lists). Lists are organized via sequential order:


```python
sample = ["this", "is", "a", "sample", "list"]
print(sample[2])
```
```
> 'a'
```

Dictionaries are unordered, and are organized via "key" and "value" pairs.

Dictionary traversal (i.e., "for" loops on dictionaries) is faster than list traversal. The difference in speed becomes quite noticeable when we deal with large datasets (e.g., frequency lists)


```python
#normed frequencies in Brown corpus
sample_d = {"the": 69033.45,"of" : 36998.52,"a": 30157.43}
print(sample_d["the"])
```
```
> 69033.45
```

```python
#iterate over keys:
for x in sample_d:
    print(x) #prints keys
```
```
> the
> of
> a
```


```python
#iterate over keys:
for x in sample_d:
    print(sample_d[x]) #prints value for each key
```
```
> 69033.45
> 36998.52
> 30157.43
```

### Adding items to dictionaries:


```python
sample_d["and"] = 28466.39
print(sample_d)
```
```
> {'the': 69033.45, 'of': 36998.52, 'a': 30157.43, 'and': 28466.39}
```

### Uses for dictionaries

I most often use dictionaries for storing word/value (e.g., frequency values, lemma form, POS, etc.) pairs.

Note that dictionary values can be strings, integers, floats, lists, tuples, or other dictionaries!



## Part II: Tuples
Tuples are storage and retrieval objects (like lists). The main difference between tuples and lists is that tuples are **immutable**. This means that while you can ADD items (but only using "+", and only tuples) to tuples, you can't CHANGE a tuple item. I do not use tuples often in my own programming, but there are popular Python packages (e.g., NLTK) that use them.


```python
sample_t = (1,2)
sample_t = sample_t + (3,4)
print(sample_t)
```
```
> (1, 2, 3, 4)
```

```python
sample_l = [1,2,3,4]
sample_l[1] = "two"
print(sample_l)
```
```
> [1, 'two', 3, 4]
```

```python
print(sample_t[1])
```
```
> 2
```

```python
sample_t[1] = "two"
```
```
> ---------------------------------------------------------------------------
>
> TypeError                                 Traceback (most recent call last)
>
> <ipython-input-40-ec2ffd9bc0a6> in <module>()
> ----> 1 sample_t[1] = "two"
>
>
> TypeError: 'tuple' object does not support item assignment
```

## Part III: Functions
An important mantra in programming is **"Don't Repeat Yourself"**, or **DRY**. The opposite of this is often called "WET" ("write everything twice", "we enjoy typing" or "waste everyone's time").  
Functions allow us to follow the DRY principle  
Functions also helps with debugging because errors will occur in the function instead of in multiple places in your code

**NOTE: I did NOT learn functions early in my programming career... which led to really long scripts, time-consuming debugging, and lots of wasted time**

# Writing functions:

All functions begin with a "def" statement that includes the name of the function and the arguments the function takes. Below is an example of a simple function (safe_divide()) that takes two arguments (a numerator and a denominator) and divides them. Note that the argument names in a function are local variables (much like in a loop). The last line in the function is a return() statement, which tells the function what to output. Return statements are not strictly necessary, but are common features of functions.

**Example 1: safe_divide()**

```python
def safe_divide(numerator,denominator): #this function has two arguments
    if denominator == 0: #if the denominator is 0
        output = 0 #the the output is 0
    else: #otherwise
        output = numerator/denominator #the output is the numerator divided by the denominator

    return(output) #return output
```
I include the safe_divide() function in almost all of my programs because Python will throw a ZeroDivisionError error if you try to divide a numerator by zero (for example, if you are comparing word frequencies across two corpora and a word occurs 532 times in corpus A, but doesn't occur in corpus B):

```python
value = 532/0
print(value)
```
```
Traceback (most recent call last):

  File "<ipython-input-1-97589f112e88>", line 1, in <module>
    value = 532/0

ZeroDivisionError: division by zero
```
But, if we use safe_divide() we won't get an error:
```python
value = safe_divide(532,0)
print(value)
```
```
> 0
```

**Example 2: reg_past()**
The reg_past() function (see below) takes a string and determines (imperfectly) whether the string is an English regular past tense verb (i.e., ends in -ed).
```python
def reg_past(word):
    past = False #set default value to False
    if len(word) > 2: #if the string is longer than two characters
        if word[-2:] == "ed": #if the final two characters are "ed"
            past = True
    return(past) # return the value for past (True or False)
```
```python
ex1 = reg_past("programmed")
print(ex1)
```
```
> True
```
```Python
ex2 = reg_past("programs")
print(ex2)
```
```
> False
```
We can also, of course, use functions within functions. Below, we will create a function that takes one argument (a sentence string), converts the string to a list of words, and calculates the proportion of words that are in the past tense. Our program won't be perfect (we will deal with some of the issues that arise in later tutorials), but it will provide an example of the kinds of things we tend to do in corpus analyses.
```python
def past_prop(sent_string):
    counter = 0 #this variable will be used to count instances of past tense verbs
    sent_list = sent_string.split(" ") #split the string into a list of words
    print(sent_list) #this is printed to show what the program is doing
    for word in sent_list: #this will loop through all of the words in our sentence
        if reg_past(word) == True: #if the word has an "ed" ending
            print("past tense:",word) #print past tense words
            counter += 1
    nwords = len(sent_list) #this counts the number of words in the sentence
    proportion = safe_divide(counter,nwords) #this will be the proportion of "ed" words in the sentence
    return(proportion) #return the proportion
```
```python
prop = past_prop("I climbed many rocks this summer.")
print(prop)
```
```
> ['I', 'climbed', 'many', 'rocks', 'this', 'summer.']
> past tense: climbed
> 0.16666666666666666
```
## Part IV: Files
Reading and writing files are both important aspects of conducting corpus analyses. Fortunately, both are straightforward in Python. Note that you must be sure to **SET YOUR WORKING DIRECTORY!** to avoid issues.


### Writing a file
To write and read files, we use the open() function. By default, the open() function will read and write files in UTF-8.


```python
x = open("test_file.txt", "w") #this creates and opens a new file (called "test_file.txt") using the "w" (write) mode. It will be written to your working directory
```
After creating the file, we can write content (strings) to the file:

```python
sample_string = "This is an awesome example sentence.\n\nNote that I can use a newline character to insert hard returns."
x.write(sample_string) #this writes a string to our newly created file
x.flush() #strings are first written to a buffer. The buffer writes to the file when it is full, so we have to make sure that we manually push everything out of the buffer when we are done writing
x.close() #this closes the file
```
If we check in our working directory, we should now see a file called "test_file.txt" that includes two lines of text.

### Opening a file
To read files, we use the .read() method of the open() function. Files that are read are interpreted as strings. Again, files are opened as UTF-8. If any characters are not compatible with UTF-8, then Python will throw an error. Below, we open the file that we just created:


```python
new_file = open("test_file.txt").read()
print(new_file)
```
```
This is an awesome example sentence.

Note that I can use a newline character to insert hard returns.
```

### Writing a spreadsheet file
We can easily write a .csv (comma separated values) or .tsv (tab separated values) spreadsheet (which can be read by spreadsheet software such as Excel).

Below, we create a simple comma-delimited spreadsheet:


```python
sample_d = {"the": 69033.45,"of" : 36998.52,"a": 30157.43} #baby normed frequency list
sample_spread = open("test_spreadsheet.csv", "w") #create .csv file
#first we write the header:
sample_spread.write("Word,Frequency") #note that the values are separated by ","
for stuff in sample_d:
    outstring = "\n" + stuff + "," + sample_d[stuff] # newline character ("\n") + key + separator + value + newline character
    sample_spread.write(outstring)

sample_spread.flush()
sample_spread.close()
```
The spreadsheet should now be in your working directory!

[Back to Tutorial Index](py_index.md)

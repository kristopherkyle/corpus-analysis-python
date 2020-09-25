[Back to Tutorial Index](py_index.md)  
Updated 9-21-2020
# Python Tutorial 1

### Accessing Python; Values, Variables and Functions

---
#### Prelude: Hello World
In the programming tradition, we must begin with the following program:
```python
print("Hello, World!")
```
```
> Hello, World!
```

---
#### We can run this code at least three ways
* Directly in the Python terminal (as in example above)
```python
print("Hello, World!")
```
```
> Hello, World!
```

* By saving a script <script_name.py> that includes the command and running it on the command line
```
$ python script_name.py
> Hello, World!
```
* In a Python interpreter (such as spyder)

---

#### Part I: Value types

Python has three basic types of **_values_**:
* strings
* integers
* floats

---

#### Strings
Strings are sequences of characters that are interpreted as text

Strings are defined using quotation marks (" or ')  
```python
"A string can include letters, numbers, or other characters"

'But be careful. Numbers that are represented as strings (like 9)'
'can not be added, subtracted, etc.'
```

---
#### Integers
Integers are whole numbers (i.e., have no decimal places)

Integers can be added, subtracted, multiplied, and divided.

```python
#these are integers:
1
2
3
4
```
---

#### Floats
Floats are numbers that have decimal places

When integers are divided, they are converted to floats
```python
#these are floats:
1.234
2.0
6.789
```
---

### Part 2: Defining Variables
Defining variables is quite easy in python.

They can be strings, integers, floats (and a variety of other structures)

```python
a = "this is a string"
b = 9
c = 3.2
```

##### what will happen when we run the following line of code?
```python
b + c
```

```
> 12.2
```

##### Important functions

Functions are called (used) via the following syntax:  
function(arguments)

Commonly used functions include:  
* print() - Prints variable to output
```python
test_var = "This is a string"
print(test_var)
```
```
> This is a string
```
* len() - Provides length of string (# characters) or list (# items)
```python
n_char = len(test_var)
print(n_char)
```
```
> 16
```
* str() - Converts integers and floats (and other data) to a string
```python
n_char_string = str(n_char)
print(n_char_string)
```
```
> '16'
```
* int() - Converts strings (if possible) and floats (rounds down) to integers
```python
int_nchars = int(n_char_string)
print(int_nchars)
```
```
> 16
```
* float() - Converts strings (if possible) and integers to floats
```python
float_nchars = float(n_char_string)
print(float_nchars)
```
```
> 16.0
```

#### Important Methods
Functions use objects to complete tasks.  

Methods are similar to functions, but complete operations on objects, which often changes them.  

Methods tend to be specific to particular object types.  

Some important **_string_** methods include:
* .lower() Converts all letters in a string to lower case
```python
sample_string = "This is a STRING"
l_sample_string = sample_string.lower()
print(l_sample_string)
```
```
> 'this is a string'
```
* .split() This turns strings into lists.
```python
sample_list = l_sample_string.split(" ")
print(sample_list)
```
```
> ['this', 'is', 'a', 'string']
```
```python
#but, we can split on any character (note, this deletes that character)
sample_list2 = l_sample_string.split("i")
print(sample_list2)
```
```
> ['th', 's ', 's a str', 'ng']
```

#### Combining methods and functions
So far, we have used very simple Python statements that include simple variable assignment, sometimes using a single function or method. Python statements, however, can be combined in a single line, and methods and functions can both be used.

```python
#print the result of lowering and splitting a string
print("This is a STRING".lower().split())
```
```
> ['this', 'is', 'a', 'string']
```
```python
#print the length of the list that is a result of lowering and splitting a string
print(len("This is a STRING".lower().split()))
```
```
> 4
```

### Exercises
1. Assign the following sentence to a variable called **string_sent** : Rock climbing and conducting corpus analyses in Python are my favorite activities.
2. Write a statement that prints the number of characters in **string_sent**.
3. Create a version of **string_sent** that is a list of words and assign it to a variable called **list_sent**.
4. Write a statement that prints the number of words in **string_sent**.
5. Assign the average number of characters per word to a variable called **av_chars**. (To get the average number of characters per word, divide the number of characters in the sentence by the number of words in the sentence).
6. Write a statement that prints the average number of characters per word as a string.

---
### Next up...
* lists
* tuples
* dictionaries
* functions

---

[Back to Tutorial Index](py_index.md)  
Updated 9-25-2020

# Python Tutorial 2:

### Strings, Lists, Loops, and Conditionals

## More fun with strings

#### Strings can be:
* **Indexed (using [ ]) :** _retrieve one character from a particular location in a string_
```python
sample_string = "sample"
i1 = sample_string[0] #note, index counts start at 0 NOT 1
print(i1)
> s
```
```python
i2 = sample_string[1] #second letter
print(i2)
> a
```
```python
i3 = sample_string[-1] #last letter
print(i3)
> e
```
* **Sliced (using [ : ]) :** _retrieve multiple contiguous characters from a particular location in a string_
```python
#slices
s1 = sample_string[0:1] #start at position 0, grab characters until you get to position 1
s2 = sample_string[0:2] #start at position 0, grab characters until you get to position 2
s3 = sample_string[1:-1] #start at position 1, grab characters until you get to last position
s4 = sample_string[1:] #start at position 1, grab all following characters
s5 = sample_string[:2] #start at beginning, grab characters until you get to position 2
print(s3)
> ampl
```
* **Concatenated (using "+") :** _strings can be added together to make longer strings_
```python
#concatenation
sample1 = "awesome"
sample2 = "super"
sample3 = sample2 + sample1
print(sample3)
> superawesome
```
```python
sample4 = sample2 + " " + sample1 #here we add a space
print(sample4)
> super awesome
```
* **Searched (using _in_) :** _we can check if certain characters (or character combinations) are in a string_
```python
#searching in strings
if "a" in sample1:
    print("yay!")
else:
    print("nope")
> yay!
```
```python
#searching in strings
if "a" in sample2:
    print("yay!")
else:
    print("nope")
```
```
> nope
```

## Lists
Lists are awesome.

**In Python:**  
- lists are indicated by square brackets [ ].
- items within a list of separated by commas.
- Almost any Python object can be a list item.

**Lists can be:**
* **Indexed (using [ ]) :** _retrieve one list item from a particular location in a list_
```python
#indexing
l1 = ["Windows","Mac","Linux"]
print(l1[1]) #just like strings, we can get particular list items
```
```
> Mac
```
* **Sliced (using [ : ]) :** _retrieve multiple contiguous list items from a particular location in a list_
```python
#slicing
print(l1[1:]) #just like strings, we can get multiple list items
```
```
> ['Mac', 'Linux']
```

* **Concatenated (using +) :** _combined two lists to make a longer list_
```Python
l2 = [1,2,3]
l3 = l1+l2
print(l3)
```
```
["Windows","Mac","Linux",1,2,3]
```
* **Appended (using .append()):** _add particular objects to a list_
```python
#append
l1.append("new string")
print(l1)
```
```
> ['Windows', 'Mac', 'Linux', 'new string']
```
* **Changed (using list_name[position] = x ) :** _We can replace items in certain positions in lists_
```python
#Change items
l1[0] = "rubbish"
print(l1)
```
```
> ['rubbish', 'Mac', 'Linux', 'new string']
```
* **Searched (using loops and conditionals, examples in next section) :** _we can check if certain objects are in a list_

## Conditional statements
Conditional statements are very powerful. The most commonly used conditional statement is the 'if' statement and its children, the 'elif' and 'else' statements. Conditional statements use operators (see table below).

**Python Operators:**

| Operator | Description |
|:----|---|
| **x == y** | _x is equal to y_|
| **x != y** | _x is not equal to y_
| **x > y** | _x is greater than y_
| **x < y** |  _x is less than y_
| **x >= y** | _x is greater than or equal to y_
| **x <= y** | _x is less than or equal to y_
| **x in y** | _x is a part of y_

The basic format for conditional statments is _if conditional_stmnt: do something_.
**Some examples:**
- Working with numbers
```Python
int1 = 2
if int1 < 2:
	#note that the "do something" statement is indented (by a tab or 4 spaces)
	print("The number is smaller than 2")
elif int1 == 2:
	print("The number is 2!")
else:
	print("The number is greater than two")
```
```
> The number is 2!
```
- Working with strings
```Python
#we can check to see if two string are the same
str1 = "sample string"
if str1 == "sample string":
	print("match!")
```
```
> match!
```
```python
#we can also check to see if a character is in a string
if "a" in str1:
    print("yay!")
```
```
> yay!
```
- Working with lists
```Python
#we can check to see if two lists are the same
list1 = ["this", "is", "a", "list", "of", "strings"]
if list1 == ["this", "is", "a", "list", "of", "strings"]:
	print("match!")
```
```
> match!
```
```python
#we can also check to see if an item (int, float, string, etc.) is in a list
if "list" in list1:
	print("yay!")
```
```
> yay!
```

## Loops
Loops are awesome. With conditional statements, they are the backbone of programming

**Things to remember when working with loops:**
* You can loop over any iterable item (e.g., strings, lists, tuples, and dictionaries)
* Loops use local variables, but can also use global variables. Don't confuse the two!
* You can have conditional statements inside of loops
* You can have loops inside of loops
* You must be careful with loop levels

The basic syntax for a loop is _for local_variable in iterable: do something_

**Examples**:


```python
#Creating a loop:
sl = ["a", "wonderful", "list", "this", "is"]

for x in sl: #note that 'x' is a local variable and is completely arbitrary
	print(x) #we can call the local variable
#note that the "do something" statement (i.e., print(x)) is indented by a tab (or 4 spaces)
```
```
> a
> wonderful
> list
> this
> is
```


```python
#if statements in loops
for x in sl:
	if "t" in x:
			print(x)
		else:
			continue #continue tells the loop to go to the next item
```
```
> list
> this
```

## Exercises
**1. Assign the string "This is an awesome sample sentence" to the variable _a_**

**2. Split the string into a list of words and assign it to variable b**

**3. Write a loop that prints each item in _b_**

**4. Define a new empty list and assign it to variable _c_**

**5. Write a loop that adds each item in _b_ to _c_ if the last letter in the item is "e"**

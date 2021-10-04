
# Answers to exercises at the end of Python Tutorial 2

# 1. Assign the string "This is an awesome sample sentence" to the variable a
```python
a = "This is an awesome sample sentence"
```

# 2. Split the string into a list of words and assign it to variable b
```python
b = a.split(" ")
```

# 3. Write a loop that prints each item in b
```python
for x in b:
	print(x)
```

```
This
is
an
awesome
sample
sentence
```

# 4. Define a new empty list and assign it to variable c
```python
c = []
```

# 5. Write a loop that adds each item in b to c if the last letter in the item is “e”
```python
for x in b:
	if x[-1] == "e":
		c.append(x)

print(c)
```

```
['awesome', 'sample', 'sentence']
```

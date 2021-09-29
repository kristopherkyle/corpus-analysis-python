
# Answers to exercises at the end of Python Tutorial 1

## 1. Assign the following sentence to a variable called string_sent : Rock climbing and conducting corpus analyses in Python are my favorite activities.

```python
string_sent = "Rock climbing and conducting corpus analyses in Python are my favorite activities."
```

## 2. Write a statement that prints the number of characters in string_sent.

```python
print(len(string_sent))
```

## 3. Create a version of string_sent that is a list of words and assign it to a variable called list_sent.

```python
list_sent = string_sent.split(" ")
```

## 4. Write a statement that prints the number of words in string_sent.

```python
print(len(list_sent))
```

## 5. Assign the average number of characters per word to a variable called av_chars. (To get the average number of characters per word, divide the number of characters in the sentence by the number of words in the sentence).
```python
av_chars = len(string_sent)/len(list_sent)
```

## 6. Write a statement that prints the average number of characters per word as a string.

```python
print(str(av_chars))
```

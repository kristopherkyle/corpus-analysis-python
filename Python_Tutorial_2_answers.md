## Sample scripts for the exercises in Python Tutorial 2

```python
a = "This is an awesome sample sentence"
b = a.split(" ")

for blah in b:
    if blah[-1] == "e":
        print(blah)
    else:
        continue
```
```
> awesome
> sample
> sentence
```


```python
a = "This is an awesome sample sentence"
b = a.split(" ")
c = []
for blah in b:
    if blah[-1] == "e":
        c.append(blah)
    else:
        continue
print(c)
```
```
> ['awesome', 'sample', 'sentence']
```

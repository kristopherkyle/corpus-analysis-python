# Putting Corpus Functions to Work
[Back to Tutorial Index](py_index.md)

So far, we have learned the basics of Python and have written a number of functions for analyzing corpora. In this tutorial, we will take our functions and put them to work!

This tutorial presumes:
1. That you have downloaded the [corpus_packages_updated.zip file]((https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Course-Materials/corpus_packages_updated.zip?raw=true), extracted it, and placed its contents (corpus_toolkit.py, corpus_nlp.py, and antbnc_lemmas_ver_003.txt) in your working directory (**_don't forget to set your working directory!_**).
2. That you have downloaded [this version of the Brown corpus (which includes 500 files)]((https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Course-Materials/brown_single.zip?raw=true), extracted it, and placed it in your working directory (making sure that you see the text files when you open the folder, not a "_MacOSX" folder and a "brown_single" folder)
3. That you have [installed spaCy](https://spacy.io/usage)
4. That you have installed the ["en_core_web_sm" language model](https://spacy.io/usage/models) for spaCy

### Step One: Load Packages
First, we will load our two Python scripts as packages. **_If you encounter errors, check your working directory!_**

```python
import corpus_toolkit as ct
import corpus_nlp as tg
```

### Step Two: Load the Brown Corpus and Tokenize It

```python
brown = ct.load_corpus("brown_single") #read all corpus files
print(len(brown)) #double check that there are 500 files. If not, check your directory (see point 2 above) and check your directory name

brown_tokenized = ct.tokenize(brown) #tokenize corpus
```
### Step Three: Lemmatize and N-gram Your Corpus
Follow these steps as required. Subsequent examples will use the lemmatized version of the corpus
```python
brown_lemmatized = ct.lemmatize(brown_tokenized) #create lemmatized version of the text
brown_bigrams = ct.ngrammer(brown_tokenized,2) #create bigram version
brown_trigrams = ct.ngrammer(brown_tokenized,3) #create trigram version

```
### Step Four: Generate Frequency and Range Dictionaries
Generate frequency and range lists (both normalized and not) and check the results.

__Raw frequency:__
```python
lemma_freq = ct.corpus_frequency(brown_lemmatized) #raw frequency
ct.high_val(lemma_freq) #use high_val function to see top 20 hits
```
```
the     69836
be      37689
of      36365
a       30475
and     28826
to      26126
in      21318
he      19417
have    11938
it      10932
that    10777
for     9479
i       8409
they    8217
with    7270
on      6729
she     6022
s       5927
at      5368
by      5299
```
__Normed frequency (per million words):__
```python
lemma_freq_normed = ct.corpus_frequency(brown_lemmatized, normed = True) #raw frequency
ct.high_val(lemma_freq_normed,hits=5) #limit list to 5 items
```
```
the     68285.57599698838
be      36852.269227196506
of      35557.66325577757
a       29798.426721293043
and     28186.03605145179
```
__Raw range:__
```python
lemma_range = ct.corpus_frequency(brown_lemmatized,calc = 'range') #raw frequency
ct.high_val(lemma_range,hits=5) #limit list to 5 items, note that these items occur in all 500 texts
```
```
that    500
be      500
it      500
at      500
of      500
```
__Normed range (percent of documents)__:
```python
lemma_range_normed = ct.corpus_frequency(brown_lemmatized,calc = 'range', normed = True) #raw frequency
ct.high_val(lemma_range_normed,hits=5) #limit list to 5 items
```
```
that    100.0
be      100.0
it      100.0
at      100.0
of      100.0
```
### Step Five: Conduct a Corpus Analysis (Collocation)
At this point, we can conduct a number of interesting corpus analyses, such as a collocation analysis or a keyness analysis (for the latter we would need a second corpus, see [Tutorial 6](Python_Tutorial_6.md)).

Below, we conduct a collocation analysis for the lemma "run" in the Brown corpus.

```python
run_collocates_mi = ct.collocator(brown_lemmatized,"run") #run default collocate analysis
ct.high_val(run_collocates_mi,hits = 10) #print top 10 collocates

```

```
risk    8.252463721332342
counter 7.894911716714259
home    6.925797707438317
hit     6.84307278519464
away    6.097645612280239
down    6.017247259638311
four    5.898114148752603
across  5.7909842740461865
step    5.2914964529680315
office  5.281878450406435
```

If we want to do follow up analysis (e.g., concordance searches), we can write our lemmatized files to a new directory (and then open them in a concordancing program such as AntConc).

```python
#our lemmatized corpus will be written to a directory/folder entitled "brown_single_lemmas" in our working directory
ct.write_corpus("brown_single","brown_single_lemmas",brown_lemmatized)
```

### Step Six: Tag the Brown Corpus

If we want to conduct more fine grained analyses (e.g., frequency, keyness, and/or collocation) we can use a tagged version of the corpus.

We will use the default options, but see [Tutorial 7]((Python_Tutorial_7.md) for more options.

```python
#tag the brown corpus using default settings (lemmas and upos tags)
brown_upos = tg.tag_corpus("brown_single") #this may take a while. Consider getting some coffee!
print(len(brown_upos)) #check to make sure that there are 500 files here! Otherwise, there is a problem with your directory name OR your working directory!
```

### Step Seven: Conduct Corpus Analyses with Tagged Corpus, Write Tagged Corpus to File

As before, we will run a freqency analysis, collocation analysis, and then write the corpus to a new directory (for use in concordancing programs such as AntConc).

__Frequency__
```python
upos_freq = ct.corpus_frequency(brown_upos) #raw frequency
ct.high_val(upos_freq,hits = 10) #use high_val function to see top 10 hits
```

```
the_DET 69861
-PRON-_PRON     46866
be_VERB 37800
of_ADP  36322
and_CCONJ       28889
a_DET   23069
in_ADP  20968
-PRON-_DET      17048
to_PART 15413
have_VERB       11978
```

__Collocation Analysis__
```python
run_upos_collocates_mi = ct.collocator(brown_upos,"run_VERB") #note that we have to include the appropriate tag in our search
ct.high_val(run_upos_collocates_mi,hits = 10) #use high_val function to see top 10 hits

```

```
counter_ADV     11.266439944604008
risk_NOUN       9.003405538770213
down_ADP        7.835390127336533
ca_VERB 6.691531108546774
away_ADV        6.498255619827081
across_ADP      6.184290903250136
around_ADV      6.080573399292674
step_NOUN       5.669504802216775
office_NOUN     5.582743490297491
down_PART       5.445100793110702
```

__Write Corpus to File__
```python
#write tagged corpus files to a folder/directory entitled "brown_single_tagged"
ct.write_corpus("brown_single","brown_single_tagged",brown_upos)
```

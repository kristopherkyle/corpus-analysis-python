# Tutorial 10: Extracting Information from XML
Corpora are often compiled/distributed in plain text format (e.g., UTF-8 .txt files). In this case, each file contains only the relevant text, and additional information about the text (or the words in the text) must be stored in the title of the file or in a stand-off spreadsheet.

Alternatively, some corpus compilers use eXtensible Markup Language (XML) when compiling corpora. XML is a method of formatting text that allows a corpus compiler to organize and annotate a document using tags and attributes.

Although XML corpora can be slightly more difficult to deal with than plain text corpora, they can include a wide range of annotations that the corpus user can choose to use or ignore.

It is important to note that although the formatting of XML is standard, there is a wide range of applications. In other words, while the way that tags and attributes must be used is standard, the tag and attribute names will differ widely by corpus. This means that a program designed to read an XML corpus must be adapted for the conventions of each corpus.

### Basic features of XML

An XML file includes three features: **_tags_**, **_text_**, and **_attributes_**.

- **_tags_** are enclosed within angle brackets "< >" and have a name (e.g., *\<word\>*). For each instance of a tag, there is a start tag *\<word\>* and an end tag *\<\/word\>*.
- **_text_** is anything that occurs between a start tag and an end tag. For example, the word "studied" in the following example is encoded as text: \<word\>study\<\/word\>. Note that text is NOT a required component of a tag.
- **_attributes_** can be included as part of a particular tag and consist of an attribute name and a value. For example, a *\<word\>* tag could have an attribute named *lemma*. In the case of the word "studies", the *lemma* attribute would have the value "study". Note that attribute values are in quotes (while attribute names are not). Attributes are only included in the start tag. "\<word lemma = "study"\>studied\</word\>"

The example below is a simple XML document (note that the tabs are included for readability and are NOT required for XML to work properly):
```xml
<document>
	<title>My favorite food</title>
	<text>
		<sentence_text id = "1">My favorite food is pepperoni pizza.</sentence_text>
		<sentence_tokens id = "1">
			<word lemma = "my", pos = "PRP$">My</word>
			<word lemma = "favorite", pos = "JJ">favorite</word>
			<word lemma = "food", pos = "NN">food</word>
			<word lemma = "be", pos = "VBZ">is</word>
			<word lemma = "pepperoni", pos = "NN">pepperoni</word>
			<word lemma = "pizza", pos = "NN">pizza</word>
	</text>
</document>
```
This example can be downloaded as a file entitled "favorite_sample.xml" [here](https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Course-Materials/favorite_sample.xml?raw=true).
### Working with XML in Python 3:
There are a number of Python packages that can be used to read and write XML. Perhaps the most commonly used one is **_ElementTree_**, which is part of the base Python package. The Python [documentation for the **__ElementTree__** package](https://docs.python.org/2/library/xml.etree.elementtree.html) is quite good. This tutorial draws on the official documentation, but the official documentation goes well beyond what is introduced here.

To get started, we will be using the xml text above, which should be saved in your working directory as "favorite_sample.xml". This file can be [downloaded here](https://github.com/kristopherkyle/Corpus-Methods-Intro/blob/master/Course-Materials/favorite_sample.xml?raw=true).

```python
import xml.etree.ElementTree as ET #import ElementTree as ET
tree = ET.parse('favorite_sample.xml') #read and parse .xml file

```

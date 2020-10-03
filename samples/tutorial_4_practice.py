#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:28:39 2020

@author: kkyle2
"""
#functions for Tutorial 4 (frequency lists)

#step 1: Write a function that tokenizes a file

sample_string = "This is a sample sentence. Consequently, so is this! Is this also one?"

#in order to 

#first, we will separate the punctuation marks from the other characters. There are many ways to do this, but we will start with the simple string method ".replace()"

#here is a starter punctuation list:



import glob

def load_corpus(dir_name, ending = '.txt', lower = True): #this function takes a directory/folder name as an argument, and returns a list of strings (each string is a document)
	master_corpus = [] #empty list for storing the corpus documents
	filenames = glob.glob(dir_name + "/*" + ending) #make a list of all ".txt" files in the directory
	for filename in filenames: #iterate through the list of filenames
		if lower == True:
			master_corpus.append(open(filename).read().lower()) #open each file, lower it and add strings to list
		else:
			master_corpus.append(open(filename).read())#open each file, (but don't lower it) and add strings to list

	return(master_corpus) #output list of strings (i.e., the corpus)

def load_corpus(dir_name): #this function takes a directory/folder name as an argument, and returns a list of strings (each string is a document)
	filenames = glob.glob(dir_name + "/*.txt") #make a list of all ".txt" files in the directory
	for filename in filenames: #iterate through the list of filenames
			yield(filename).read().lower()#open each file and yield a lowered string



# Import the modules
import sys
import random
import requests
from bs4 import BeautifulSoup
import string
import csv
from numpy import genfromtxt
import funcs
from recipe_scrapers import scrape_me

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

print("===============================================================")
print("=======  Recipe_cleaner:  Generating training data  ===========")
print("===============================================================")

# reading in the file with the list of web addresses ##
web_list = open('../data/web_list.dat', 'r')
web_addresses = web_list.readlines()

# overwriting and emptying the current vocab list
file = open("../data/training_data_file.csv", "w")
file.close()

for web_address in web_addresses:
    print(web_address)
    funcs.generate_training_example(web_address)




# PLAN OF ACTION
#
# Need to decompose the web page into sections
# Each section starts from (and includes) a heading, to the next heading.
# Each of these sections will be represented by a vector, whos length
# represents 10000/50000 of the most frequently used words in the recipe/ingredients
# part, and the blog part, ie:
# [0, 0, 1, 0, 1, 1, 0,  ... ,  0, 1, 1]
# where 1 prepresents a word that is in the section, and 0 when it isn't.
# These will be the training examples.


# Thoughts on sectioning a webpage:
# =================================

# It seems that sometimes the ingredients or instructions are separated by subheaders, eg:
# Instructions:
# Sauce:
#   do this, this and that
# Pasta:
#   Do that, that and this.
# Maybe I should say that if sequential sections appear to be ingredients or insturctions, put them together?


# Possible features:
# ==================

# Binary array of frequently appearing words
# Length of section
# Header of section
# Header type
# HTML tags within the section?
# 






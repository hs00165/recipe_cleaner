# Import the modules
import sys
import random
import requests
import string
from bs4 import BeautifulSoup
import csv
from numpy import genfromtxt
import funcs

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

print("===============================================================")
print("=============  Recipe_cleaner:  Vocab logger  =================")
print("===============================================================")


# reading in the file with the list of web addresses
web_list = open('../data/web_list.dat', 'r')
web_addresses = web_list.readlines()

# overwriting and emptying the current vocab list
file = open("../data/vocab_list.csv", "w")
file.close()

for web_address in web_addresses:
	print(web_address)
	funcs.log_vocab(web_address)






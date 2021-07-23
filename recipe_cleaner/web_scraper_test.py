# Import the modules
import sys
import random
import requests
import string
from bs4 import BeautifulSoup
import csv
from numpy import genfromtxt
from recipe_scrapers import scrape_me
import funcs

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


web_address = "https://www.southernliving.com/recipes/fried-catfish"

# ========================== Accessing the webpage =============================
# ==============================================================================
heading_list = []
section_list = []

page = requests.get(web_address)

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html5lib')

# ======= Generating the section lists for each section of the webpage =========
# ==============================================================================
target = soup.find_all(["h1", "h2", "h3", "h4"])

for i in range(len(target)):

	
	print("siblings:  "+str(len(target[i].find_next_siblings())))


	# If the header has siblings
	if len(target[i].find_next_siblings()) >= 1:	
		for sib in target[i].find_next_siblings():
			
			if sib.name=="h1" or sib.name=="h2" or sib.name=="h3" or sib.name=="h4":
				#print(sib.text)
				break
			else:
				print(target[i].text.strip())
				print(sib.text)
				heading_list.append(target[i].text.strip())
				section_list.append(sib.text.strip())


	# If the header has no siblings,
	# search for parents!
	if len(target[i].find_next_siblings()) == 0:
		for uncles in target[i].parent.find_next_siblings():
			if uncles.name=="h1" or uncles.name=="h2" or uncles.name=="h3" or uncles.name=="h4":
				#print(sib.text)
				break
			else:
				print(target[i].text.strip())
				print(uncles.text)
				heading_list.append(target[i].text.strip())
				section_list.append(uncles.text.strip())

# for section in section_list:
# 	print(funcs.process_section(section))




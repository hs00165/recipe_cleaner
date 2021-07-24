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


web_address = "https://www.seriouseats.com/kinilaw-5193131"

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

	exit_flag = 0
	print("siblings:  "+str(len(target[i].find_next_siblings())))


	# If the header has siblings
	if len(target[i].find_next_siblings()) >= 1 and  exit_flag==0:	
		for sib in target[i].find_next_siblings():
			
			if sib.name=="h1" or sib.name=="h2" or sib.name=="h3" or sib.name=="h4":
				exit_flag=1
				break
			else:
				print(target[i].text.strip())
				print(sib.text)
				heading_list.append(target[i].text.strip())
				section_list.append(sib.text.strip())


	# If the header has no siblings,
	# search for parents!
	if exit_flag==0:
		print("no siblings")
		for uncles in target[i].parent.find_next_siblings():
			if uncles.name=="h1" or uncles.name=="h2" or uncles.name=="h3" or uncles.name=="h4":
				exit_flag=1
				break
			else:
				print(target[i].text.strip())
				print(uncles.text)
				heading_list.append(target[i].text.strip())
				section_list.append(uncles.text.strip())


	# If the parent has no siblings,
	# search for grand parents!
	if exit_flag==0:
		print("no parents")
		for great_uncles in target[i].parent.parent.find_next_siblings():
			if great_uncles.name=="h1" or great_uncles.name=="h2" or great_uncles.name=="h3" or great_uncles.name=="h4":
				exit_flag=1
				break
			else:
				print(target[i].text.strip())
				print(great_uncles.text)
				heading_list.append(target[i].text.strip())
				section_list.append(great_uncles.text.strip())


	# If the parent has no siblings,
	# search for grand parents!
	if exit_flag==0:
		print("no g parents==========================================================================================")
		for gg_uncles in target[i].parent.parent.parent.find_next_siblings():
			if gg_uncles.name=="h1" or gg_uncles.name=="h2" or gg_uncles.name=="h3" or gg_uncles.name=="h4":
				exit_flag=1
				break
			else:
				print(target[i].text.strip())
				print(gg_uncles.text)
				heading_list.append(target[i].text.strip())
				section_list.append(gg_uncles.text.strip())


	# If the parent has no siblings,
	# search for grand parents!
	if exit_flag==0:
		print("no gg parents")
		for ggg_uncles in target[i].parent.parent.parent.parent.find_next_siblings():
			if ggg_uncles.name=="h1" or ggg_uncles.name=="h2" or ggg_uncles.name=="h3" or ggg_uncles.name=="h4":
				exit_flag=1
				break
			else:
				print(target[i].text.strip())
				print(ggg_uncles.text)
				heading_list.append(target[i].text.strip())
				section_list.append(ggg_uncles.text.strip())




	# If the parent has no siblings,
	# search for grand parents!
	if exit_flag==0:
		print("no ggg parents")
		for gggg_uncles in target[i].parent.parent.parent.parent.parent.find_next_siblings():
			if gggg_uncles.name=="h1" or gggg_uncles.name=="h2" or gggg_uncles.name=="h3" or gggg_uncles.name=="h4":
				exit_flag=1
				break
			else:
				print(target[i].text.strip())
				print(gggg_uncles.text)
				heading_list.append(target[i].text.strip())
				section_list.append(gggg_uncles.text.strip())




for section in section_list:
	print(funcs.process_section(section))

#print(soup.prettify())




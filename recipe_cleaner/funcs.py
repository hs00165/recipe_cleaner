# Import the modules
import sys
import random
import requests
import string
from bs4 import BeautifulSoup
import csv
from numpy import genfromtxt
from recipe_scrapers import scrape_me

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def ingredients_match_score(section_list, final_ingredients_list, toggle_score_method):

	score = 0

	if toggle_score_method == 1:
		if len(final_ingredients_list) != 0:

			for word3 in final_ingredients_list:
				if word3 in section_list:
					score += 1
			score = score*100/(1.*len(final_ingredients_list))

	if toggle_score_method == 2:
		if len(section_list) != 0:

			for word3 in section_list:
				if word3 in final_ingredients_list:
					score += 1
			score = score*100/(1.*len(section_list))

	return score


def get_section_list(web_address):
	# ========================== Accessing the webpage =============================
	# ==============================================================================
	heading_list = []
	section_list = []

	page = requests.get(web_address)

	# Create a BeautifulSoup object
	soup = BeautifulSoup(page.text, 'html.parser')

	# ======= Generating the section lists for each section of the webpage =========
	# ==============================================================================
	target = soup.find_all(["h1", "h2", "h3", "h4"])

	for i in range(len(target)):
	    for sib in target[i].find_next_siblings():
	        if sib.name=="h1" or sib.name=="h2" or sib.name=="h3" or sib.name=="h4" :
	            break
	        else:
	            heading_list.append(target[i].text.strip())
	            section_list.append(sib.text)

	return section_list

def get_heading_list(web_address):
	# ========================== Accessing the webpage =============================
	# ==============================================================================
	heading_list = []
	section_list = []

	page = requests.get(web_address)

	# Create a BeautifulSoup object
	soup = BeautifulSoup(page.text, 'html.parser')

	# ======= Generating the section lists for each section of the webpage =========
	# ==============================================================================
	target = soup.find_all(["h1", "h2", "h3", "h4"])

	for i in range(len(target)):
	    for sib in target[i].find_next_siblings():
	        if sib.name=="h1" or sib.name=="h2" or sib.name=="h3" or sib.name=="h4" :
	            break
	        else:
	            heading_list.append(target[i].text.strip())
	            section_list.append(sib.text)

	return heading_list


def get_ingredients(web_address):
	# ======= Getting the ingredients list using the recipe_scraper library ========
	# ==============================================================================
	ingredients_list = []
	individual_ingredients_list = []
	condensed_ingredients_list = []
	final_ingredients_list = []

	scraper = scrape_me(web_address)
	ingredients_list = scraper.ingredients()
	instructions_list = scraper.instructions()

	# Editting the ingredients list to have no punctuation and use stemming
	# - splitting the ingredients into a list of strings
	for ingredient in ingredients_list:
	    temp_list = ingredient.split()
	    for temp_word in temp_list:
	        individual_ingredients_list.append(temp_word)
	# - Removing all punctuation from the strings
	for word in individual_ingredients_list:
	    condensed_ingredients_list.append(word.translate(str.maketrans('', '', string.punctuation)))
	# - Stemming the strings to simpler terms
	ps = PorterStemmer()
	for word2 in condensed_ingredients_list:
	    final_ingredients_list.append(ps.stem(word2))

	return final_ingredients_list

def process_section(section):
    condensed_section_text = [] # Section after getting rid of punctuation
    final_section_text = [] # Section words after stemming is applied
    # Splitting the webpage text into a list of strings
    section_text = section.split()

    # === Editting the page text to have no punctuation and use stemming ====
    # =======================================================================
    # Removing all punctuation from the string
    for word in section_text:
        condensed_section_text.append(word.translate(str.maketrans('', '', string.punctuation)))
    # Stemming the strings to simpler terms
    ps = PorterStemmer()
    for word1 in condensed_section_text:
    	# the clean_string function takes out any non-alphanumeric characters 
    	word2 = clean_string(ps.stem(word1))
    	final_section_text.append(word2)

    return final_section_text


def clean_string(input_string):
	acceptable_characters = ["a","b","c","d","e","f","g","h","i","j",
	"k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
	"1","2","3","4","5","6","7","8","9","0"]
	output_string = ""

	for element in input_string:
		for character in acceptable_characters:
			if element == character:
				output_string = output_string + element

	return output_string





def log_vocab(web_address):
	initial_vocab_list = []
	initial_vocab_frequency = []
	final_page_text = []

	# =======================================================================
	# ==========  Deconstructing webpage and logging vocabulary =============
	# =======================================================================

	# ============= Pulling and processing text from webpage ================
	# =======================================================================
	section_list = get_section_list(web_address)
	heading_list = get_heading_list(web_address)

	for section in section_list:
		processed_section = process_section(section)
		final_page_text.extend(processed_section)


	# ==================== Pulling the vocabulary log =======================
	# =======================================================================
	with open('../data/vocab_list.csv', 'r', encoding='utf-8-sig') as VocabFile:    
		csvReader = csv.reader(VocabFile)    
		for row in csvReader:        
			initial_vocab_list.append(row[0])
			initial_vocab_frequency.append(int(row[1]))        


	# ========= Appending webpage string list to vocabulary log =============
	# =======================================================================
	vocab_list_count = 0
	page_text_count = 0
	append_to_list = 1

	for i in final_page_text:
		vocab_list_count = 0
		append_to_list = 1

		for j in initial_vocab_list:

			if i == j:
				initial_vocab_frequency[vocab_list_count] += 1
				append_to_list = 0
				break
			vocab_list_count += 1

		if append_to_list == 1:
			initial_vocab_list.append(i)
			initial_vocab_frequency.append(1)  

		page_text_count += 1


	# ======= Writing the new vocabulary log back to the .csv file ==========
	# =======================================================================
	new_vocab_list = list(zip(initial_vocab_list, initial_vocab_frequency))

	with open('../data/vocab_list.csv', 'w', encoding='UTF8', newline='') as NewVocabFile:
		writer = csv.writer(NewVocabFile)
		writer.writerows(new_vocab_list)



def generate_training_example(web_address):

	# ========================== Accessing the webpage =============================
	# ==============================================================================
	section_list = get_section_list(web_address)
	heading_list = get_heading_list(web_address)

	# ======= Getting the ingredients list using the recipe_scraper library ========
	# ==============================================================================
	final_ingredients_list = get_ingredients(web_address)

	# =========================================================================
	# Looping through each section, extracting the individual words and scoring 
	# them based on their similarity to the recipe_scrapers ingredients list.
	# =========================================================================
	section_count = 0
	sim_score_record_count = 0
	sim_score_record = 0.
	section_matrix = []
	comb_sim_score = []

	for section in section_list:
	    # = Editting the section to have no punctuation, use stemming be form a list =
	    # ============================================================================
	    final_section_text = process_section(section)
	    section_matrix.append(final_section_text)

	    # Determining the "ingredient similarity score" using two methods, and taking
	    # their product for the final score.
	    sim_score1 = ingredients_match_score(final_section_text, final_ingredients_list, 1)
	    sim_score2 = ingredients_match_score(final_section_text, final_ingredients_list, 2)
	    comb_sim_score.append(sim_score1*sim_score2)
	    if sim_score1*sim_score2 > sim_score_record:
	        sim_score_record = sim_score1*sim_score2
	        sim_score_record_count = section_count
	    section_count += 1

	with open('../data/training_data_file.csv', 'a', newline='') as training_data_file:
	    csvwriter = csv.writer(training_data_file)
	    section_count = 0
	    for section in section_matrix:
	        if section_count == sim_score_record_count:
	            section.insert(0,web_address)
	            section.insert(0,comb_sim_score[section_count])
	            section.insert(0,1)
	            csvwriter.writerow(section)
	        else:
	            section.insert(0,web_address)
	            section.insert(0,comb_sim_score[section_count])
	            section.insert(0,0)
	            csvwriter.writerow(section)
	        section_count += 1

	print(sim_score_record)


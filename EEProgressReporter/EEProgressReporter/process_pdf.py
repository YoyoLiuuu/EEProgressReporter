import textract #for extract text from PDF
from PyPDF2 import PdfFileReader, PdfFileWriter #reading pdf and completing multiple tasks with pdf
from pathlib import Path #for using path
import pdfplumber #for extracting word in individual pages


def title_page_detect(pdf_path): #for detecting title page
	page_text = []
	file_base_name = pdf_path.replace('.pdf', '')

	pdf_writer = PdfFileWriter() #write pdf

	the_path = (
		Path.home()
		/ pdf_path
 	)#get path in correct format

	input_pdf = PdfFileReader(str(the_path))#create object for reading pdf

	number_of_pages = input_pdf.getNumPages()#get number of pages in the pdf

	if number_of_pages >= 2:
		possible_page = 2 #get the two pages
		pdf_writer.addPage(input_pdf.getPage(0))
		pdf_writer.addPage(input_pdf.getPage(1))#copy page 1 and 2 into the new document
		other = [[], []] #create separate list for different pages
		title_page_exist = [[False, False], False] #initialize title page existence: not existing on both pages, not "real" title
	if number_of_pages == 1:
		possible_page = 1
		pdf_writer.addPage(input_pdf.getPage(0))#copy pages into a new document
		other = [[]] #just 1 list within the list
		title_page_exist = [False, False] #initialize title page existence: not existing on the page, not "real" title

	with open('title_page.pdf'.format(file_base_name),'wb') as f:
		pdf_writer.write(f) 
		f.close()#write the copied pages into the newly created pdf
	
	for i in range(possible_page):
		pdf = pdfplumber.open('title_page.pdf')
		page = pdf.pages[i]
		text_on_page = page.extract_text()
		pdf.close() #extract all text from the pdf page
		page_text.append(text_on_page.split())#make texts into list of string
		
		if 5 <=len(page_text[i]) <= 80:
			title_page_exist[0][i] = True #when the word count is between 5 and 80 words, then it pass the first check
			if "Table of Contents" in text_on_page or "Table Of Contents" in text_on_page or "TABLE OF CONTENTS" in text_on_page or "........" in text_on_page or ". . . . . . . ." in text_on_page: 
				#make sure the short page is not table of content
				other[i].append("toc")
			if "Coursework confirmation" in text_on_page: #make sure IB first page is not mis-calculated as title page
				other[i].append("IB_title")

	for i in range(len(other)):
		if len(other[i]) == 0:#if the two pages are not others
			title_page_exist[1] = True #then declare second variable true
	
	if possible_page == 2:
		if title_page_exist[0][1] and title_page_exist[0][1]:
			title_page_exist[0] = True
		else: 
			title_page_exist[0] = False 
	'''check if both pages meet the between 5 to 80 words standard, so the program does not mistakenly take one page's 
		word count as true and the other page's non-existence of Table of Contents as true and delare the presence of title page'''

	if title_page_exist[0] and title_page_exist[1]: #if both variable is true (less word + not others)
		yes_title_page = True #then there is a title page
	else: 
		yes_title_page = False #if not, then title page doesn't exist 

	return yes_title_page 


def word_count(text):
	num_words = len(text)
	return num_words #count word

def detect(text, toc, bibliography):
	toc_exist = False 
	bibliography_exist = False #initiate both variable as false

	for i in range(len(text)): #go through every word and check if a word/words is bibliography of table of contents
		if (text[i] == b'bibliography:' or text[i] == b'Bibliography:' or text[i] == b'BIBLIOGRAPHY:' or text[i] == b'References:' or text[i] == b'references:' or text[i] == b'REFERENCES:' 
			or text[i] == b'Sources:'or text[i] == b'sources:'or text[i] == b'SOURCES:' or text[i] == b'bibliography' or text[i] == b'Bibliography' or text[i] == b'BIBLIOGRAPHY' or text[i] == b'References' or text[i] == b'references' or text[i] == b'REFERENCES' 
			or text[i] == b'Sources'or text[i] == b'sources'or text[i] == b'SOURCES' or ((text[i] == b'Work' or text[i] == b'work' or text[i] == b'WORK' or text[i] == b'Works' or text[i] == b'works' or text[i] == b'WORKS') 
				and (text[i+1] == b'cited' or text[i+1] == b'Cited' or text[i+1] == b'CITED' or text[i+1] == b'cited:' or text[i+1] == b'Cited:' or text[i+1] == b'CITED:') )) and bibliography:
			bibliography_exist = True 
		elif (text[i] == b"table" or  text[i] == b"Table" or text[i] == b"TABLE") and toc: 
			if text[i+1] == b"of" or text[i+1] == b"Of" or text[i+1] == b"OF":
				if text[i+2] == b"Contents:" or text[i+2] == b"contents:" or text[i+2] == b"CONTENTS:" or text[i+2] == b"Contents" or text[i+2] == b"contents" or text[i+2] == b"CONTENTS": 
					#the three words table of contents has to be together
					try: 
						for j in range(i, i+90): #after word "table", there needs to be row of dot present after it
							if (b"........" in text[j]) or (b". . . . . . . ." in text[j]) or (b"--------"): #has to have .... in table of contents, cannot just be talking about it in the essay
								toc_exist = True
								break #break the loop so it does not need to go through all the words after it
					except:
						toc_exist = False #change value to false if does not meet further requirements
		
	return toc_exist, bibliography_exist 

def get_word_progress(word, weigh): 
	#get progress for word count base on number of words, weigh is the rate of importance the user inputted
	if word >= 3500:
		return 1*weigh
	if 2500 <= word < 3500:
		return 0.75*weigh
	if 1500 <= word < 2500:
		return 0.5*weigh
	if 500 <= word < 1500:
		return 0.25*weigh
	if word < 500:
		return 0 # return percentage of individual section base on word count

def get_progress(existence, weigh): 
	#for all progress base on presence, just return 0 when not available and the value of the weighting when present
	if existence == True:
		return weigh 
	else:
		return 0


def calculate_progress(list_of_want, list_of_have, list_of_weigh):
	#list of want: store whether the user want to detect a feature
	#list of have: store the features detected and their value 
	#list of weigh: store how much they count towards the final report

	for i in range(0, len(list_of_weigh)):
		#print(list_of_weigh) #uncomment to see the list of weigh for debug purposes
		if not list_of_weigh[i]:
			list_of_weigh[i] = 0 #turn value that does not have weighting count none
		else:
			list_of_weigh[i] = int(list_of_weigh[i]) #turn string to integer for calculation
	

	sum_of_all = sum(list_of_weigh) #get sum of all weighting
	all_progress = [] #make a empty list for all progress
	

	if list_of_want[0] == 'Yes':
		word_weigh = list_of_weigh[0]/sum_of_all 
		#make weighting a decimal so later it is easier to turn into a percent
		word_progress = get_word_progress(list_of_have[0], word_weigh) #
		all_progress.append(word_progress) #if they want word progress, get word progress with weighting
	
	for i in range(1, 4):
		if list_of_want[i] == 'Yes':
			current_weigh = list_of_weigh[i]/sum_of_all
			all_progress.append(get_progress(list_of_have[i], current_weigh)) 
			#for everything that involves detecting presence, get their weighting base on presence

	
	total_progress = "{:.0%}".format(sum(all_progress)) 
	#add progress together for all progress and format it ad percentage

	return total_progress, all_progress


def the_main(path, tableOfContents, tocroi, word, wcroi, titlePage, tproi, bibliography, broi):
	all_wanted = [word, tableOfContents, titlePage, bibliography]#store whether one feature want to be detected or not
	all_feature_detected = ['', '', '', '']#placeholder before actual value came in
	weighting = [wcroi, tocroi, tproi, broi]#get weighting together

	all_text = textract.process(path, method='pdftotext')#get text extrated from the pdf
	text = all_text.split()#change all text into a list of string

	if word == 'Yes':
		total_words = word_count(text)#count word if client
		all_feature_detected[0] = total_words #change feature to the detected feature

	if titlePage == 'Yes': 
		titlePage_presence = title_page_detect(path) #detect title page if client want it to count towards the report
		all_feature_detected[2] = titlePage_presence #change third item in all_feature_detected to the presence of title page

	toc_presence, bibliography_presence = detect(text, tableOfContents, bibliography) #detect toc and presence of bibliography together

	if tableOfContents == 'Yes':
		all_feature_detected[1] = toc_presence #only record it in all_feature_detected if user want it to be present
	
	if bibliography == 'Yes':
		all_feature_detected[3] = bibliography_presence #only record it in all_feature_detected if user want it to be present
	
	#by the end, there should be two lists: all wanted, containing whether the user want a feature. all_feature_detected, the actual existence/value of the features
	
	#print(all_wanted, all_feature_detected) #uncomment this one to see whether this ^ are functioning properly
	
	#order: total_words, toc_presence, titlePage_presence, bibliography_presence -> the order of items in the list
	total_progress, individual_progress = calculate_progress(all_wanted, all_feature_detected, weighting) #calculate the all process
	#print(total_progress, individual_progress, all_feature_detected) #uncomment to display all process in terminal for debugging purpose

	return total_progress, individual_progress, all_feature_detected #return the progress and list for display
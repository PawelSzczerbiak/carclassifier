from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import os
import re

page_base = 'https://www.motofakty.pl/'
page_opinions = 'https://www.motofakty.pl/samochody/opinie/'

# Cars
#cars = ['ssangyong', 'lancia', 'hyundai', 'kia', 'skoda', 'fiat', \
# 'ford', 'renault', 'volkswagen', 'nissan,' 'opel', 'peugeot', \
# 'citroen', 'mazda', 'mitsubishi']

'''
Extracts opinions and their labels for specific link.
Returns a tuple (labels, opinions, next_link), where
next link redirects to the subpage with labels and opinions 
that shall be extracted afterwards.
'''
def extract_opinions(link):

	# Parameters to be returned
	labels = []
	opinions = []
	next_link = False

	response = urllib.request.urlopen(link)
	page_source = response.read().decode('utf-8')
	soup = BeautifulSoup(page_source, 'html.parser')

	# Extract labels and opinions
	opinions_wrapper = soup.find_all(class_="tresc")
	for child in opinions_wrapper:
		labels.append(child.find('img').get('title'))
		opinions.append(child.find("p").get_text())

	# Get next link
	links_wrapper = soup.find(class_="stronicowanie").find_all('a')
	for child in links_wrapper:
		if(child.get('title') == 'Następna strona'):
			next_link = urllib.parse.urljoin(page_base, child.get('href')) # next link

	return (labels, opinions, next_link)

'''
Purifies opinion string.
'''
def opinion_preprocessing(opinion):
	# Get rid of the phrase at the begining
	opinion = opinion.replace('Podsumowanie: ', '')
	# Opinion as a single line (remove all whitespaces inside)
	opinion = re.sub('\s+',' ',opinion) + '\n'
	return opinion

def main():

	for car in cars:

		print('Extracting data for ' + car)

		# Create two files for specific car type 
		# one for positive and one for negative opinion
		file_pos = open('data/pos/' + car, 'w')
		file_neg = open('data/neg/' + car, 'w')

		# Base link
		next_link = urllib.parse.urljoin(page_opinions, car)

		while(next_link):
			(labels, opinions, next_link) = extract_opinions(next_link)
			
			for label, opinion in zip(labels, opinions):
				opinion = opinion_preprocessing(opinion)
				# Long opinions use to be too detailed 
				# and do not contain worth information
				if len(opinion) > 200:
					continue
				if 'nie kupiłby' in label:
					file_neg.write(opinion)
				else:
					file_pos.write(opinion)

if __name__ == '__main__':
	main()
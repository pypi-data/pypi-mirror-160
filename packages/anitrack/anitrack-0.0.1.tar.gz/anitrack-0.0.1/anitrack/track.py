import requests
from bs4 import BeautifulSoup
import urllib.parse as parse
import re
import argparse

from deep_translator import GoogleTranslator

def translate(lang, text):
	return GoogleTranslator(source='auto', target=lang).translate(text)

def about(lang, name):
	search_url = ("https://www.anime-planet.com/anime/" + name)
	source_code = requests.get(search_url)
	content = source_code.content
	soup = BeautifulSoup(content, features="html.parser")

	info = soup.find('div', {'class': 'pure-1 md-3-5'})
	ttext = info.find('p').getText()
	return translate(lang, ttext)

def episodes(name):
	search_url = ("https://www.anime-planet.com/anime/" + name)
	source_code = requests.get(search_url)
	content = source_code.content
	soup = BeautifulSoup(content, features="html.parser")

	total_episodes = soup.find('div', {'class': 'pure-1 md-1-5'})
	ttext = re.sub("[^0-9]", "", total_episodes.find('span').getText())
	return ttext

def years(name):
	search_url = ("https://www.anime-planet.com/anime/" + name)
	source_code = requests.get(search_url)
	content = source_code.content
	soup = BeautifulSoup(content, features="html.parser")

	active_years = soup.find('span', {'class': 'iconYear'})
	ttext = active_years.getText()
	return ttext

def rating(lang, name):
	search_url = ("https://www.anime-planet.com/anime/" + name)
	source_code = requests.get(search_url)
	content = source_code.content
	soup = BeautifulSoup(content, features="html.parser")

	rating = soup.find('div', {'class': 'avgRating'})
	ttext = rating.find('span').getText()
	return translate(lang, ttext)

def tags(lang, name):
	search_url = ("https://www.anime-planet.com/anime/" + name)
	source_code = requests.get(search_url)
	content = source_code.content
	soup = BeautifulSoup(content, features="html.parser")

	tags = soup.find('div', {'class': 'tags'})

	list = []
	for _ in range(4):
		list.append(tags.find('ul').getText())

	ttext = list[0].replace("\n\n", "")

	return translate(lang, ttext)

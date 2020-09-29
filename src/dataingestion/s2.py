import requests
from bs4 import BeautifulSoup
import json
import unicodedata
import re


baseurl = 'https://dumps.wikimedia.org/enwiki/'

index = requests.get(baseurl).text
soup_index = BeautifulSoup(index, 'html.parser')

links = []
for file in soup_index.find_all('a'):
    text = file.text
    links.append(text)

latestfolder = links[-2]
currentDumpURL = baseurl + latestfolder

index = requests.get(currentDumpURL).text
soup_index = BeautifulSoup(index, 'html.parser')

print(currentDumpURL)
files = []
for file in soup_index.find_all(href=re.compile("articles-multistream[0-9][0-9]")):
        text = file.text
        files.append(text)

#print(files)
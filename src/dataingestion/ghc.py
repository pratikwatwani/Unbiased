import requests
from bs4 import BeautifulSoup
import os
import re
import unicodedata
from datetime import datetime
import logging
import time


baseurl = 'https://live.gracehoppercelebration.com/recruitment/'

index = requests.get(baseurl).text
soup_index = BeautifulSoup(index, 'html.parser')

soup_index.find_all('tr')

print(soup_index)
import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime
import logging
import time

from linkGenerator import *


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#os.chdir('/home/ubuntu/EBWE/src/dataingestion/lists')

def linkScraper(baseurl):
    """This function uses beautiful to generate the filenames for the intended data to be downloaded

    Args:
        baseurl (string): The base url or root directory of the data dump directory hosted by Wikipedia
    """
    index = requests.get(baseurl).text
    soup_index = BeautifulSoup(index, 'html.parser')
    pastDumpURL = baseurl + 'latest/'
    dump_html = requests.get(pastDumpURL).text
    soup_dump = BeautifulSoup(dump_html, 'html.parser')

    Pfiles = []

    for file in soup_dump.find_all('a'):
        text = file.text
        if 'stub-meta-history' in text:
            Pfiles.append(text)

    links = []
    for file in soup_index.find_all('a'):
        text = file.text
        links.append(text)

    latestfolder = links[-2]
    currentDumpURL = baseurl + latestfolder

    index = requests.get(currentDumpURL).text
    soup_index = BeautifulSoup(index, 'html.parser')

    Cfiles = []
    for file in soup_index.find_all(href=re.compile("articles-multistream[0-9][0-9]")):
        text = file.text
        Cfiles.append(text)

    linkGenerator(file = Pfiles, url=pastDumpURL, name = 'historic')
    linkGenerator(file = Cfiles, url=currentDumpURL, name='current')

if __name__ == "__main__":
    logging.info('initiating program')
    start = time.time()
    linkScraper('https://dumps.wikimedia.org/enwiki/')
    print("Total time for execution: {}".format(time.time()-start))
    
    
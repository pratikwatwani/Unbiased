import requests
from bs4 import BeautifulSoup
import os
import re
import unicodedata
from datetime import datetime
import logging
import time

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#os.chdir('/home/ubuntu/EBWE/src/dataingestion/lists')

def getlist(baseurl):
    """This function using scraping generates text files of download links for both current and past Wikipedia datadump

    Args:
        baseurl (string): The base url or root directory of the data dump directory hosted by Wikipedia
    """
    index = requests.get(baseurl).text
    soup_index = BeautifulSoup(index, 'html.parser')
    dump_url = baseurl + 'latest/'
    dump_html = requests.get(dump_url).text
    soup_dump = BeautifulSoup(dump_html, 'html.parser')

    soup_dump.find_all('li', {'class': 'file'})
    Pfiles = []

    for file in soup_dump.find_all('a'):
        text = file.text
        if 'stub-meta-history' in text:
            Pfiles.append(text)

    Pfiles = [unicodedata.normalize('NFKD', file).encode('ascii', 'ignore') for file in Pfiles]
    historic_files = [i for i in Pfiles if i.endswith('.gz')]

    url = 'https://dumps.wikimedia.org/enwiki/latest/'
    historic_url_generator = [url+i for i in historic_files]

    try:
        logging.info('Generating historic data set resource link')
        with open("historic_urls.txt", 'w+') as f:
            for item in historic_url_generator:
                f.write("%s\n" % item)
        logging.info('Resource links generated in historic_urls.txt in the files folder')
    except Exception as e:
        logging.error(e)


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

    current_url_generator = [currentDumpURL+i for i in Cfiles]

    try:
        logging.info('Generating current data set resource link')
        with open("current_urls.txt", 'w+') as f:
            for item in current_url_generator:
                f.write("%s\n" % item)
        logging.info('Resource links generated in current_urls.txt in the files folder')
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    logging.info('initiating program')
    start = time.time()
    downloadlist = getlist('https://dumps.wikimedia.org/enwiki/')
    print("Total time for execution: {}".format(time.time()-start))
    
    
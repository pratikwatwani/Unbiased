import unicodedata
from fileWriter import *

def linkGenerator(file, url, name):
    """This function generates url links to all files scraped from the Wikipedia data dump website

    Args:
        file (list): list of all file names intended for download
        url (string): root url of the Wikipedia directory 
        name (string): name to be given to the final file write
    """
    file = file
    directoryurl = url
    filename = name

    
    if isinstance(file[0], unicode):
        file = [unicodedata.normalize('NFKD', f).encode('ascii', 'ignore') for f in file]
    if file[0].endswith('.gz'):
        file = [f for f in file if f.endswith('.gz')]
   
    file = [directoryurl+i for i in file]

    fileWriter(file, filename)
    
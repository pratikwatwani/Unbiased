import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def fileWriter(list, filename):
    """This function writes the urls links generated in the linkGenerator() to txt files

    Args:
        list (list): list of all urls
        filename (name): name to be given to the final file write
    """
    linklist = list
    filename = filename+'_urls.txt'
    try:
        logging.info('Generating {} data set resource link'.format(filename))
        with open(filename, 'w+') as f:
            for item in linklist:
                f.write("%s\n" % item)
        logging.info('Resource links generated in {} in the files folder'.format(filename))
    except Exception as e:
        logging.error(e)
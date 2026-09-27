import logging
import csv
import sys

from HGNC_search import settings

# Custom exceptions
class FileEmptyError(Exception):
    pass
class HeaderError(Exception):
    pass

# create a logger for model
logger = logging.getLogger(__name__)

def extract_file_data(filename):
    """
    Read the HGNC txt file and retrieve the relevant information and store in dictionary structure for application.
    
    Args: 
        filename: str 
            Path to the data file.
    
    Returns:
        data: list 
            A List of gene information dictionaries
    """

    logger.info("Reading data from file")

    # Try to open the file
    try:
        with open(filename) as f:
            contents = csv.reader(f, delimiter='\t') 
            rows = list(contents) # Create a list containing contents of each row
    # If FileNotFoundError raised, update log and raise error
    except FileNotFoundError:
        logger.error("File not found")
        logger.critical("Program aborted")
        raise
    
    # Check if file was empty, if True raise error
    if not rows:
        logger.error("File empty")
        logger.critical("Program aborted")
        raise FileEmptyError("File is empty")

    # Call function to extract data from list and return subsequent list
    return parse_data(rows)

def parse_data(l):
    """
    Extract relevant data from a list into a lightweight data structure

    Args:
        l: list
            List of data to filer
    Returns:
        d: list
            List of info in dictionaries
    """
    # List to store gene info dictionaries
    data = []

    # Create a dict containing the relevant headings and the column index in tsv (supported by copilot output)
    template_dict = {
        heading: index
        for index, heading in enumerate(l[0])
        if heading in settings.fields
    }

    # If file header did not contain any of desired fields dict will be empty
    if not template_dict:
        logger.error("File contents not valid")
        logger.critical("Program aborted")
        raise HeaderError("File header does not contain any desired fields or delimiter not tab")

    # Check that list contains more than header row
    if not l[1:]:
        logger.error("File only contains header row")
        logger.critical("Program aborted")
        raise FileEmptyError("File only contains header row")

    # Including fields in log for debugging
    for field in template_dict.keys():
        logger.debug(f'gene info for "{field}" will be stored')

    # For rest of rows, extract the relevant values for each heading (supported by copilot output)
    for row in l[1:]:
        gene_info = {
            heading: row[index]
            for heading, index in template_dict.items()
        }
        data.append(gene_info)

    return data
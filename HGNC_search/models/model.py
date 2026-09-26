import logging
import csv
import sys

from HGNC_search import settings

# Custom exception
class FileEmpty(Exception):
    pass

# create a logger for model
logger = logging.getLogger(__name__)

def extract_file_data(filename):
    """
    Read the HGNC txt file and retrieve the relevant information and store in dictionary structure for application.
    
    Args: 
        filename: Path to the data file.
    
    Returns:
        List: A List of gene information dictionaries
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
        raise FileEmpty("File is empty")


    # Sort file contents into lightweight data structure
    # List to store gene info dictionaries
    data = []

    # Create a dict containing the relevant headings and the column index in tsv (supported by copilot output)
    template_dict = {
        heading: index
        for index, heading in enumerate(rows[0])
        if heading in settings.fields
    }

    # Including fields in log for debugging
    for field in template_dict.keys():
        logger.debug(f'gene info for "{field}" will be stored')

    # For rest of rows, extract the relevant values for each heading (supported by copilot output)
    for row in rows[1:]:
        gene_info = {
            heading: row[index]
            for heading, index in template_dict.items()
        }
        data.append(gene_info)
    
    return data

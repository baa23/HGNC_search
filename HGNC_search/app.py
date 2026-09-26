import logging

from HGNC_search import settings
from HGNC_search.logger import setup_logging
from HGNC_search.models import model

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application started")

    # File is defined in settings
    DATA_FILE = settings.DATA_FILE

    # Retrieve contents of file
    gene_data = model.extract_file_data(DATA_FILE)
    if gene_data:
        logger.info("File read successfully")

if __name__ == "__main__":
    main()
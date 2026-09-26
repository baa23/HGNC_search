from flask import Flask, request, render_template
import logging

from HGNC_search import settings
from HGNC_search.logger import setup_logging
from HGNC_search.models import model

def initialise_app():
    """
    Create and configure the Flask application

    Returns:
        Flask: Configured Flask application instance
    """
    # Set-up logging for application and create named logger for app.py
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application started")

    # Create app instance
    app: Flask = Flask(__name__)

    # Assign file as defined in settings
    DATA_FILE = settings.DATA_FILE

    # Retrieve contents of file and store in app config
    logger.info("Loading data file")

    try:
        app.config["DATA"] = model.extract_file_data(DATA_FILE)
        logger.info("File read successfully")
    except Exception:
        logger.exception("Failed to load data")
        raise
    
    @app.route("/")
    def home():
        """
        Render the homepage

        """
        logger.debug("Rendering homepage")
        return render_template("index.html")

    return app




# Import time app instance (for mounting to gunicorn or mod_wsgi)
app: Flask = initialise_app()

if __name__ == "__main__":
    app.run()

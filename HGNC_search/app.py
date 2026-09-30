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
    
    @app.route("/search", methods=["POST"])
    def search():
        """
        Perform gene searches.

        Returns:
            str: Rendered template containing results or error messages.
        """

        # Retrieve response from form
        try:
            gene = request.form.get("gene", "").strip().upper()
            logger.debug(f"Received search request for gene: {gene}")
        
            # Check response is not empty
            if not gene:
                logger.warning("No gene provided in request")
                return render_template(
                    "index.html",
                    output_text_1="ERROR: No gene provided",
                )
            
            search_type = request.form.get("search_type", "")

            # Check only numbers submitted if searching using HGNC: ID
            if search_type == "hgnc_id":
                if not gene.isdigit():
                    logger.warning("Incorrect HGNC ID format submitted")
                    return render_template(
                    "index.html",
                    output_text_1="ERROR: ID must only include digits",
                )
            
            # Check gene symbol starts with a letter if searching using gene symbol
            if search_type == "gene_symbol":
                if not gene[0].isalpha():
                    logger.warning("Incorrect gene symbol format submitted")
                    return render_template(
                        "index.html",
                        output_text_1="ERROR: Human gene symbols must start with a letter",
                    )

            data = app.config["DATA"]
            result = model.find_gene(gene, search_type, data)

            if not result:
                return render_template(
                    "index.html",
                    output_text_1= f"{gene} not found",
                )
            
            output = []
            for key, value in result.items():
                s = key + (" " * 3) + ">>" + (" " * 3) + value
                output.append(s)
                output_final  = "\n".join(output)
            
            return render_template(
                    "index.html",
                    output_text_1= output_final,
                )
            
        except Exception as e:
            logger.exception("Unexpected error during search")
            return render_template(
                "index.html",
                output_text_1=f"ERROR: {str(e)}",
            )

    return app


# Import time app instance (for mounting to gunicorn or mod_wsgi)
app: Flask = initialise_app()

if __name__ == "__main__":
    app.run(debug=True)

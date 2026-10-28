# MCR Project Assignment

## HGNC Search Application
This project is a flask based web application which allows searching for gene information from HGNC. This has been developed as part of the Bioinformatics Foundational Unit requirements.

Users can enter either a gene symbol (e.g. *CFTR*) or a HGNC ID (e.g. HGNC:1884) to search for relevant information about that gene from HGNC data. Information return will include as below, (where available):
- hgnc_id
- gene_symbol
- gene_name
- previous_symbols
- previous_names
- aliases
- mane_select transcript
- mane_plus_clinical transcript(s)

---

## Data Source

The application uses a locally stored copy of the HGNC data "hgnc_complete_set.txt" available from:

https://storage.googleapis.com/public-download-files/hgnc/tsv/tsv/hgnc_complete_set.txt

This data file is included within the application repository in the data folder (downloaded 3rd September 2026). This could be replaced with an updated version of the file.

---

## Application configuration

The application uses a docker container (with python v3.12.8). Packages are installed and managed using pip (via requirements.txt). Project configuration and metadata are defined in pyproject.toml.

---

# Installation

First clone the repository locally and run the testing suite.

# Testing

Before launching the application check that install has been successful by running the unit and UI tests. These scripts are within the test folder and can be automatically run using pytest. 

Run the complete unit and UI test suite:

```bash
pytest
```

Run the test suite with coverage:

```bash
pytest \
    --cov=HGNC_search \
    --cov-report=term-missing:skip-covered \
    --cov-report=html \
    --cov-report=xml
```

An interactive HTML coverage report is generated in:

```text
htmlcov/index.html
```

---
# Docker

This application is run within a docker container, this requires docker (docker engine) to be installed. Follow instructions below for docker install. If an updated HGNC data set is required download this from the link above and replace the file in the data folder. This new file must be named "hgnc_complete_set.txt".

## 0. Docker Install
If docker is not already installed you can download it from here:
https://docs.docker.com/engine/install/

Choose the appropriate install for your OS and follow instructions to install Docker Engine.

## 1. Create the Docker Image
Create the docker image that will be used for the application container. The docker image is created from the Dockerfile within the repository.

```bash
docker build -t hgnc .
```

## 2. Launch the application within the docker container
The docker container is created from the image which launches the flask application on port 8000.

```bash
docker run -p 8000:8000 hgnc
```

---

# Shutting down

Stop the Flask development server using:

```text
Ctrl+C
```

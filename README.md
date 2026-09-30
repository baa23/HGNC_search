# MCR Project Assignment

[![.github/workflows/tests.yml](https://github.com/baa23/HGNC_search/actions/workflows/tests.yml/badge.svg?branch=readme_badges)](https://github.com/baa23/HGNC_search/actions/workflows/tests.yml)

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

The application uses a conda environment to specify the python version required (via environment.yml). Packages are installed and managed using pip (via requirements.txt). Project configuration and metadata are defined in pyproject.toml.

---

# Installation

Once the application repository has been cloned locally, the conda environment should be created and activated before installing the dependancies and project using pip. If an updated HGNC data set is required download this from the link above and replace the file in the data folder. This new file must be named "hgnc_complete_set.txt".

## 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

## 2. Activate the environment

```bash
conda activate hgnc
```

## 3. Install the project

```bash
pip install -e .
```

The editable installation allows changes made to the source code to be immediately reflected without reinstalling the package.

## 4. Check dependancies

```bash
pip list
```
Check the packages in the list match those in requirments.txt and install anything that has been missed.

---

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

# Launching the application

Start the Flask development server with:

```bash
python -m HGNC_search.app
```

Alternatively, the application can be run directly from the source file:

```bash
python HGNC_search/app.py
```

The application will be available at:

```text
http://127.0.0.1:5000/
```

---

# Shutting down

Stop the Flask development server using:

```text
Ctrl+C
```

Deactivate the Conda environment when finished:

```bash
conda deactivate
```

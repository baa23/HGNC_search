import pytest
from typing import Iterator
from flask.testing import FlaskClient


from HGNC_search.app import app

@pytest.fixture
def client():
    """
    Create a Flask test client for the application.

    Yields
        FlaskClient
            Configured test client for sending requests.
    """
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

# ------------------------------------------------------------------
# Home route tests
# ------------------------------------------------------------------

def test_home_page_status(client: FlaskClient):
    """
    Test that the home page returns HTTP 200.
    """
    response = client.get("/")
    assert response.status_code == 200

    html = response.data.decode()
    assert "<html" in html.lower()


# ------------------------------------------------------------------
# Search route tests
# ------------------------------------------------------------------

def test_search_valid_gene(client: FlaskClient):
    """
    Test submitting a valid gene symbol returns expected output.
    """
    response = client.post(
        "/search",
        data={"gene": "CFTR", "search_type": "gene_symbol"}
    )

    assert response.status_code == 200

    html = response.data.decode()
    assert "symbol" in html
    assert "CFTR" in html
    assert "1884" in html

def test_search_valid_id(client: FlaskClient):
    """
    Test submitting a valid gene id returns expected output.
    """
    response = client.post(
        "/search",
        data={"gene": "1884", "search_type": "hgnc_id"}
    )

    assert response.status_code == 200

    html = response.data.decode()
    assert "symbol" in html
    assert "CFTR" in html
    assert "1884" in html

def test_search_blank(client: FlaskClient):
    """
    Test submitting blank request returns user error message
    """
    response = client.post(
        "/search",
        data={"gene": " ", "search_type": "gene_symbol"}
    )

    assert response.status_code == 200

    html = response.data.decode()
    assert "ERROR" in html or "No gene" in html

def test_search_invalid_gene(client: FlaskClient):
    """
    Test submitting number at start of symbol returns user error message
    """
    response = client.post(
        "/search",
        data={"gene": "53dna", "search_type": "gene_symbol"}
    )

    assert response.status_code == 200

    html = response.data.decode()
    assert "ERROR" in html and "letter" in html


def test_search_invalid_id(client: FlaskClient):
    """
    Test submitting non-number in ID search returns user error message
    """
    response = client.post(
        "/search",
        data={"gene": "dna", "search_type": "hgnc_id"}
    )

    assert response.status_code == 200

    html = response.data.decode()
    assert "ERROR" in html and "digit" in html

def test_search_gene_not_found(client: FlaskClient):
    """
    Test submitting with gene not in database returns "not found" message
    """
    response = client.post(
        "/search",
        data={"gene": "dna", "search_type": "gene_symbol"}
    )

    assert response.status_code == 200

    html = response.data.decode()
    assert "not found" in html

def test_search_id_not_found(client: FlaskClient):
    """
    Test submitting with id not in database returns "not found" message
    """
    response = client.post(
        "/search",
        data={"gene": "666", "search_type": "hgnc_id"}
    )

    assert response.status_code == 200

    html = response.data.decode()
    assert "not found" in html
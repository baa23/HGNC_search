import pytest
from pathlib import Path

from HGNC_search.models import model
from HGNC_search.models.model import FileEmptyError
from HGNC_search.models.model import HeaderError
from HGNC_search import settings

# ------------------------------------------------------------------
# extract_file_data tests
# ------------------------------------------------------------------

def test_file_valid(tmp_path: Path):
    """
    Should return expected result when passing valid file to function
    """
    fields = settings.fields
    file = tmp_path / "test_data.txt"
    # Create tsv dummy data using the desired fields
    line = "\t".join(["test"] * len(fields))
    file.write_text("\t".join(fields) + "\n" + line + "\n")

    # create expected result
    result = []
    expected = {
        field: "test"
        for field in fields
    }
    result.append(expected)

    assert result == model.extract_file_data(file)

def test_file_not_found(tmp_path: Path):
    """
    Should return FileNotFound error when file non-existent
    """
    file = tmp_path / "no_file.txt"

    with pytest.raises(FileNotFoundError):
        model.extract_file_data(file)

def test_file_empty(tmp_path: Path):
    """
    Should return FileEmpty error when file is empty
    """
    file = tmp_path / "empty.txt"
    file.write_text("")

    with pytest.raises(FileEmptyError):
        model.extract_file_data(file)

def test_file_delimiter_invalid(tmp_path: Path):
    """
    Should return HeaderError when delimiter used is not tab
    """
    fields = settings.fields
    file = tmp_path / "wrong_delimiter.txt"
    # Create non-tsv dummy data using the desired fields
    file.write_text("-".join(fields) + "\n")

    with pytest.raises(HeaderError):
        model.extract_file_data(file)

# ------------------------------------------------------------------
# parse_data tests
# ------------------------------------------------------------------

def test_parse_data_valid():
    """
    Should return the expected result when passing valid list to function
    """
    fields = settings.fields
    lines = [
        fields,
        ["one"] * len(fields),
        ["two"] * len(fields),
    ]

    # create expected result
    expected = [
        {field: "one" for field in fields},
        {field: "two" for field in fields},
    ]

    assert expected == model.parse_data(lines)
    
def test_data_no_relevant_fields():
    """
    Should return HeaderError when header row does not contain any of desired fields
    """
    # List structure that would be passed to parse_data
    lines = [
        "fruit\taisle\tprice".split("\t"),
        "apple\t10\t1.5".split("\t"),
    ]

    with pytest.raises(HeaderError):
        model.parse_data(lines)

def test_data_only_header():
    """
    Should return the FileEmptyError when only header row in file
    """
    lines = [
        settings.fields
    ]

    with pytest.raises(FileEmptyError):
        model.parse_data(lines)

# ------------------------------------------------------------------
# find_gene tests
# ------------------------------------------------------------------

def test_find_gene_valid_gene():
    """
    Should return info for gene when symbol valid
    """
    gene = "CFTR"
    search_type = "gene_symbol"
    dataset = [
        {"hgnc_id":"HGNC:5", "symbol":"A1BG"},
        {"hgnc_id":"HGNC:1884", "symbol":"CFTR"}
    ]

    result = model.find_gene(gene, search_type, dataset)

    assert result
    assert result["hgnc_id"] == "HGNC:1884"
    assert result ["symbol"] == "CFTR" 

def test_find_gene_valid_hgnc_id():
    """
    Should return info for gene when HGNC ID valid
    """
    gene = "1884"
    search_type = "hgnc_id"
    dataset = [
        {"hgnc_id":"HGNC:5", "symbol":"A1BG"},
        {"hgnc_id":"HGNC:1884", "symbol":"CFTR"}
    ]

    result = model.find_gene(gene, search_type, dataset)

    assert result
    assert result["hgnc_id"] == "HGNC:1884"
    assert result ["symbol"] == "CFTR" 

def test_find_gene_not_found():
    """
    Should return None when gene symbol not found
    """
    gene = "becky"
    search_type = "gene_symbol"
    dataset = [
        {"hgnc_id":"HGNC:5", "symbol":"A1BG"},
        {"hgnc_id":"HGNC:1884", "symbol":"CFTR"}
    ]

    result = model.find_gene(gene, search_type, dataset)

    assert not result

def test_find_id_not_found():
    """
    Should return None when gene symbol not found
    """
    gene = "666"
    search_type = "gene_symbol"
    dataset = [
        {"hgnc_id":"HGNC:5", "symbol":"A1BG"},
        {"hgnc_id":"HGNC:1884", "symbol":"CFTR"}
    ]

    result = model.find_gene(gene, search_type, dataset)

    assert not result



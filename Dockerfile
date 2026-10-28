FROM python:3.12.8

WORKDIR /HGNC_search

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "HGNC_search.app"]
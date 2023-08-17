from worker.celery import app
from worker.provider_scraper.fetcher import DataFetcher


@app.task
def process_fetch():
    data_fetcher = DataFetcher("http://localhost:5000")
    data_fetcher.fetch_and_parse()

from worker.celery import app
from worker.provider_scraper.fetcher import DataFetcher


@app.task
def process_fetch():
    data_fetcher = DataFetcher("https://provider.code-challenge.feverup.com/api/events", "1")
    data_fetcher.fetch_and_parse()

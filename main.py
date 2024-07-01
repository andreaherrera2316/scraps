from datetime import datetime, timedelta
from entities.scrape_request.scrape_request import ScrapeRequest
from formatters.ymd_formatter import ymd_format_date
from formatters.iso_formatter import iso_format_date
from scraps import Scraps

API_KEY = ""
tor = False
start = datetime.now() - timedelta(days=30)
end = datetime.now()
interval = timedelta(days=7)

# Scrape Site Info
url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key={API_KEY}"
payload = {}
request_sample = ScrapeRequest(url, payload)
formatter = ymd_format_date
start_key = "start_date"
end_key = "end_date"
scraps_legit = Scraps(
    url=url,
    payload=payload,
    formatter=formatter,
    interval=interval,
    start=start,
    end=end,
    start_key=start_key,
    end_key=end_key,
    tor=tor,
    back_in_time=True,
    multiple_files=True,
)
scraps_legit.run()

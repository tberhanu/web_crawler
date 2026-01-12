import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Fetcher:
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def fetch(self, url: str) -> str | None:
        try:
            resp = requests.get(url, timeout=self.timeout, headers={"User-Agent": "MyCrawler"})
            if resp.status_code != 200:
                return None
            if "text/html" not in resp.headers.get("Content-Type", ""):
                return None
            return resp.text
        except requests.RequestException:
            return None



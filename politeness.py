import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class PolitenessManager:
    def __init__(self, min_delay: float = 1.0):
        self.min_delay = min_delay
        self.last_fetch_time = {}       # domain -> timestamp
        self.robots = {}                # domain -> RobotFileParser

    def _get_domain(self, url: str) -> str:
        return urlparse(url).netloc

    def can_fetch(self, url: str, user_agent: str = "MyCrawler") -> bool:
        domain = self._get_domain(url)
        if domain not in self.robots:
            robots_url = f"https://{domain}/robots.txt"
            rp = RobotFileParser()
            try:
                rp.set_url(robots_url)
                rp.read()
            except Exception:
                rp = RobotFileParser()   # default allow-all if error
                rp.parse(["User-agent: *", "Disallow:"])
            self.robots[domain] = rp
        #  Calls the parser's built-in method to check if the user agent is allowed
        #  to fetch that URL according to robots.txt rules
        return self.robots[domain].can_fetch(user_agent, url)

    def wait_if_needed(self, url: str):
        domain = self._get_domain(url)
        now = time.time()
        last = self.last_fetch_time.get(domain, 0)
        elapsed = now - last
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_fetch_time[domain] = time.time()

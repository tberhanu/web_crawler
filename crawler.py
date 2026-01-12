from frontier import Frontier, UrlTask
from parser import Parser
from fetcher import Fetcher
import time
from politeness import PolitenessManager
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, seeds: list[str], max_depth: int = 2, min_delay: float = 1.0):
        self.frontier = Frontier(max_depth=max_depth)
        for url in seeds:
            self.frontier.add(UrlTask(url=url, depth=0))

        self.politeness = PolitenessManager(min_delay=min_delay)
        self.fetcher = Fetcher()
        self.parser = Parser()

    def crawl(self, max_pages: int = 100, timeout_seconds: int = 30):
        pages_crawled = 0
        results = []
        start_time = time.time()

        while not self.frontier.is_empty() and pages_crawled < max_pages:
            if time.time() - start_time > timeout_seconds:
                print(f"Crawl timeout reached after {timeout_seconds}s")
                break
            task = self.frontier.get_next()
            if task is None:
                break

            if not self.politeness.can_fetch(task.url):
                continue

            self.politeness.wait_if_needed(task.url)
            html = self.fetcher.fetch(task.url)
            if html is None:
                continue

            data = self.parser.extract_data(task.url, html)
            results.append(data)
            pages_crawled += 1

            links = self.parser.extract_links(task.url, html)
            for link in links:
                self.frontier.add(UrlTask(url=link, depth=task.depth + 1, parent_url=task.url))

        return results

if __name__ == "__main__":
    try:
        seeds = ["https://example.com", "https://example.org"]
        crawler = Crawler(seeds=seeds, max_depth=1, min_delay=1.0)
        pages = crawler.crawl(max_pages=50, timeout_seconds=30)
        for p in pages:
            print(p["url"], "->", p["title"])
            print(p["content"][:200], "...\n")
    except KeyboardInterrupt:
        print("\nCrawl interrupted by user")
    except Exception as e:
        print(f"Error during crawl: {e}")
        import traceback
        traceback.print_exc()
        print("-----------------------------------")

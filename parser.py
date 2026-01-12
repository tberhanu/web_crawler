from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Parser:
    def extract_links(self, base_url: str, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            links.append(urljoin(base_url, a["href"]))
        return links

    def extract_data(self, url: str, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        # Title
        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # Try to find main content
        content = self._extract_main_content(soup)

        return {
            "url": url,
            "title": title,
            "content": content,
        }

    def _extract_main_content(self, soup):
        # 1. Look for <article>
        article = soup.find("article")
        if article:
            return article.get_text(separator="\n", strip=True)

        # 2. Look for <main>
        main = soup.find("main")
        if main:
            return main.get_text(separator="\n", strip=True)

        # 3. Fallback: extract all <p> tags
        paragraphs = soup.find_all("p")
        if paragraphs:
            text = "\n".join(p.get_text(strip=True) for p in paragraphs)
            return text

        # 4. Last resort: whole page text
        return soup.get_text(separator="\n", strip=True)

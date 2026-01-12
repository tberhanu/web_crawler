# Web Crawler

A low-level design implementation of a web crawler built in Python. This crawler systematically fetches and parses web pages while respecting robots.txt rules and politeness constraints.

## Features

- **URL Frontier Management**: BFS-based queue with depth tracking and duplicate prevention
- **Politeness Enforcement**: Respects robots.txt rules and enforces minimum delay between requests
- **Content Extraction**: Extracts page titles, links, and main content (articles, paragraphs, etc.)
- **Error Handling**: Graceful handling of network errors, timeouts, and malformed content
- **Configurable Limits**: Set maximum depth, pages to crawl, and request delays

## Project Structure

```
web_crawler/
├── crawler.py          # Main crawler orchestrator
├── frontier.py         # URL queue and visited tracking
├── fetcher.py          # HTTP request handling
├── parser.py           # HTML parsing and data extraction
├── politeness.py       # robots.txt compliance and rate limiting
└── README.md           # This file
```

## Components

### Frontier (`frontier.py`)
Manages the URL queue and visited URLs to avoid duplicates and enforce depth limits.

- `add(task)`: Add URL task to queue if not visited and within depth limit
- `get_next()`: Retrieve next URL to crawl (FIFO)
- `is_empty()`: Check if queue is exhausted

### Fetcher (`fetcher.py`)
Handles HTTP requests with proper headers and error handling.

- `fetch(url)`: Downloads page HTML with timeout protection
- Returns `None` if fetch fails or content is not HTML

### Parser (`parser.py`)
Extracts data from HTML content.

- `extract_links(base_url, html)`: Find all links and resolve relative URLs
- `extract_data(url, html)`: Extract title and main content

### PolitenessManager (`politeness.py`)
Enforces web crawling ethics and robots.txt compliance.

- `can_fetch(url)`: Check if URL is allowed by robots.txt
- `wait_if_needed(url)`: Enforce minimum delay between requests to same domain

### Crawler (`crawler.py`)
Main orchestrator that coordinates all components.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
pip install beautifulsoup4 requests
```

## Usage

Basic usage:

```python
from crawler import Crawler

# Initialize with seed URLs
crawler = Crawler(
    seeds=["https://example.com"],
    max_depth=2,          # Crawl up to 2 levels deep
    min_delay=1.0         # Wait 1 second between requests to same domain
)

# Start crawling
pages = crawler.crawl(
    max_pages=50,         # Crawl max 50 pages
    timeout_seconds=30    # Stop after 30 seconds
)

# Process results
for page in pages:
    print(f"URL: {page['url']}")
    print(f"Title: {page['title']}")
    print(f"Content: {page['content'][:200]}...")
```

Run from command line:

```bash
python crawler.py
```

## Configuration

Adjust crawler behavior by modifying these parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_depth` | 2 | Maximum crawling depth from seed URLs |
| `min_delay` | 1.0 | Seconds to wait between requests to same domain |
| `max_pages` | 100 | Maximum number of pages to crawl |
| `timeout_seconds` | 30 | Overall crawl timeout in seconds |
| `fetcher.timeout` | 10.0 | HTTP request timeout per page |

## Example Output

```
https://example.com -> Example Domain
This domain is for use in documentation examples without needing permission. Avoid use in operations...

https://example.org -> Example Domain
This domain is for use in documentation examples without needing permission. Avoid use in operations...
```

## Design Patterns

- **BFS (Breadth-First Search)**: Frontier uses FIFO queue for systematic page discovery
- **Caching**: Robots.txt files cached per domain to avoid re-fetching
- **Rate Limiting**: Per-domain request throttling for politeness

## Error Handling

The crawler gracefully handles:
- Network timeouts
- HTTP errors (404, 500, etc.)
- Non-HTML content types
- Invalid URLs
- Robots.txt fetch failures (defaults to allow-all)
- Keyboard interrupts

## Requirements

- Python 3.10+
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP requests

## Notes

- This is an educational implementation of web crawler concepts
- Always respect websites' `robots.txt` and `Terms of Service`
- Use appropriate delays to avoid overloading servers
- Consider robots.txt guidelines for your user agent

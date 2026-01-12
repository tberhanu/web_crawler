from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass
class UrlTask:
    url: str
    depth: int
    parent_url: str | None = None


class Frontier:
    def __init__(self, max_depth: int):
        self.queue = []
        self.visited = set()
        self.max_depth = max_depth

    def add(self, task: UrlTask):
        if task.depth > self.max_depth:
            return
        if task.url in self.visited:
            return
        self.visited.add(task.url)
        self.queue.append(task)

    def get_next(self) -> UrlTask | None:
        if not self.queue:
            return None
        return self.queue.pop(0)

    def is_empty(self) -> bool:
        return len(self.queue) == 0

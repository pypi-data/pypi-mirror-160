import math

from collections import deque
from queue import Full, Empty
from threading import Event


class Queue:
    _queue = None

    def __init__(self, maxsize: int = 0):
        self._maxsize = maxsize if maxsize > 0 else math.inf
        self._has_items = Event()
        self._queue = deque()

    def get(self, block: bool = True, timeout: float = None):
        if not block:
            timeout = 0
        result = self._has_items.wait(timeout=timeout)
        if not result:
            raise Empty

        try:
            return self._queue.popleft()
        except IndexError:
            self._has_items.clear()
            return self.get(block=block, timeout=timeout)

    def put(self, item):
        if len(self._queue) >= self._maxsize:
            raise Full

        self._queue.append(item)

        if not self._has_items.is_set():
            self._has_items.set()

    def putleft(self, item):
        if len(self._queue) >= self._maxsize:
            raise Full

        self._queue.appendleft(item)

        if not self._has_items.is_set():
            self._has_items.set()

    def empty(self) -> bool:
        return not self._queue

    def full(self) -> bool:
        return len(self._queue) >= self._maxsize

    def qsize(self):
        """This method is not necesarily thread safe"""
        return len(self._queue)

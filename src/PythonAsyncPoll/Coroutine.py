from __future__ import annotations
from typing import Any, Callable, List
from dataclasses import dataclass

class CoroutineLocals:
    """Dummy container for locals we want to share across functions called in coroutine"""
    pass

@dataclass
class Pollfd:
    """Corresponds to C struct pollfd"""
    fd: int
    events: int
    revents: int

class Coroutine:
    def __init__(self, callables: List[Callable[[Coroutine], Any]]) -> None:
        self.callables = callables
        self.current_callable_index: int = 0
        self.awaiting_fd: bool = False
        self.pollfd = Pollfd(-1, -1, -1)
        self.coroutine_locals = CoroutineLocals();

    @property
    def has_finished(self) -> bool:
        return self.current_callable_index == len(self.callables)

    def run(self) -> None:
        """ Return True if poll requested else False for all done """
        while not self.has_finished:
            callable_ = self.callables[self.current_callable_index]
            self.current_callable_index += 1

            self.awaiting_fd = False
            callable_(self)
            if self.awaiting_fd: # poll requested by callable_
                return

    def await_fd(self, fd: int, events: int) -> None:
        self.pollfd.fd = fd
        self.pollfd.events = events
        self.awaiting_fd = True

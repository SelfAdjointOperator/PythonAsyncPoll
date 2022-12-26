from typing import List
import select

from .Coroutine import Coroutine

class EventLoop:
    def __init__(self, coroutines: List[Coroutine]) -> None:
        self.coroutines = coroutines

    def run(self) -> None:
        while True:
            coroutines_to_poll: List[Coroutine] = []

            for coroutine in self.coroutines:
                if coroutine.has_finished:
                    continue

                # if cpu-runnable, run
                if not coroutine.awaiting_fd:
                    coroutine.run()
                    if coroutine.has_finished:
                        # ran to completion
                        continue

                # coroutine awaiting; poll its fd
                coroutines_to_poll.append(coroutine)

            if not coroutines_to_poll:
                # all coroutines finished
                break

            poller = select.poll()
            for coroutine in coroutines_to_poll:
                poller.register(coroutine.pollfd.fd, coroutine.pollfd.events)

            for ready_fd, ready_fd_revents in poller.poll():
                for coroutine in coroutines_to_poll:
                    if coroutine.pollfd.fd == ready_fd:
                        coroutine.pollfd.revents = ready_fd_revents
                        coroutine.awaiting_fd = False

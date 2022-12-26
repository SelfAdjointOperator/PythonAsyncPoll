# PythonAsyncPoll

A simple example of the foundations for an `asyncio`-like library

A coroutine `coroutine` runs its `callables` functions until one of the functions calls `coroutine.await_fd(fd, events)`. This sets a flag on the coroutine to tell the event loop to suspend execution of the coroutine until the file descriptor `fd` has one of the events in the bitwise int `events` pending for it. When an event loop has no cpu-runnable coroutines left, it uses `poll` from the `select` module (the C equivalent being under `<sys/poll.h>`) to poll the blocked coroutines' file descriptors. When file descriptors are ready, the event loop resumes execution of the next callables for the corresponding coroutines, one coroutine at a time.

In reality, a language designer may want to concatenate all the functions in `callables` together. This makes handling local variables easier than the user saving them between function calls manually. This could be achieved say by introducing a keyword `await` with the syntax `await (coroutine, fd, events)` to replace `coroutine.await_fd(fd, events)`, which could save stack-states similarly to `yield` in Python.

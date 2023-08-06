import multiprocessing


def runner(modname, taskname, send, *args, **kwargs):
    from importlib import import_module

    module = import_module(modname)
    task = getattr(module, taskname)

    result = task.function(*args, **kwargs)
    send.send(result)


class Result:
    def __init__(self, recv):
        self.recv = recv

    def poll(self, timeout=None):
        return self.recv.poll(timeout)

    def get(self, timeout=None):
        if self.poll(timeout):
            return self.recv.recv()
        raise TimeoutError("Result is not available.")


class Task:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs):
        recv, send = multiprocessing.Pipe(duplex=False)
        process = multiprocessing.Process(
            target=runner,
            args=(self.function.__module__, self.function.__name__, send, *args),
            kwargs=kwargs,
            daemon=True,
        )
        process.start()
        return Result(recv)


def task(function):
    return Task(function)

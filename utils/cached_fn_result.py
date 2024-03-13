from .job import Job
from typing import Callable, Union


class CachedFunctionResult:
    def __init__(self):
        self.cache_box = {}

    def run_fn(self, fn: Union[Callable, Job]):
        if isinstance(fn, Job):
            fn.start()
            return fn
        j = Job(target=fn)
        j.start()
        return j

    def instant_run_fn(self, fn: Union[Callable, Job]):
        if isinstance(fn, Job):
            return fn._target(**fn._kwargs)
        return fn()

    def queue(self, name: str, fn: Union[Callable, Job]):
        if name not in self.cache_box or len(self.cache_box[name]) == 0:
            self.cache_box.setdefault(name, [])
            self.cache_box[name].append(self.run_fn(fn))
            return self.instant_run_fn(fn)
        else:
            self.cache_box[name].append(self.run_fn(fn))
            return self.cache_box[name].pop(0).get_result(True)

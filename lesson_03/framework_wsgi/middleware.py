from typing import Any, Iterable, Callable, List, Tuple


class Middleware:
    pre_process_funcs: List[Callable] = []
    post_process_funcs: List[Callable] = []

    @staticmethod
    def pre_process(func: Callable):
        Middleware.pre_process_funcs.append(func)
        return func

    @staticmethod
    def post_process(func: Callable):
        Middleware.post_process_funcs.append(func)
        return func


middleware = Middleware()

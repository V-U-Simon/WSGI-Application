from time import time

from framework_wsgi.http.response import Response


def debug(method):
    def wrapper(*args, **kwargs):
        time_start = time()
        result = method(*args, **kwargs)
        if isinstance(result, Response):
            print(
                f"Debug log {method.__name__} ({result.request.url}) spent -> {(time() - time_start):2.2f} ms"
            )
        else:
            print(
                f"Debug log {method.__name__} spent -> {(time() - time_start):2.2f} ms"
            )
        return result

    return wrapper


if __name__ == "__main__":

    @debug
    def add_one(number):
        return number + 1

    res = add_one(1)
    print(res)

from time import time


def debug(method):
    def wrapper(*args, **kwargs):
        time_start = time()
        result = method(*args, **kwargs)
        print(f"Debug log {method.__name__} spent -> {(time() - time_start):2.2f} ms")
        return result

    return wrapper


if __name__ == "__main__":

    @debug
    def add_one(number):
        return number + 1

    res = add_one(1)
    print(res)

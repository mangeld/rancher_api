import string
from functools import wraps


class dummy_lru_cache:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped

def process(previous, current, next_chr):
    uppercase = string.ascii_uppercase
    if not previous and current in uppercase:
        return current.lower()
    if previous and current in uppercase and previous in uppercase:
        return current.lower()
    if current in uppercase:
        return ["_", current.lower()]
    return current

def uncamelize(word):
    result = list()

    for index, char in enumerate(word):
        previous = word[index - 1] if index > 0 else None
        next_chr = word[index + 1] if index < len(word) - 1 else None
        result.append("".join(process(previous, char, next_chr)))
    return "".join(result)

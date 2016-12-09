import string


def uncamelize(word):
    result = list()
    uncamelized = False
    for char in word:
        if char in string.ascii_uppercase:
            if uncamelized:
                uncamelized = False
                result.append(char.lower())
                continue
            result.append("_")
            result.append(char.lower())
            uncamelized = True
        else:
            result.append(char)
    return "".join(result)

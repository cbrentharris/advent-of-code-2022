def chain(i, *functions):
    result = i
    for f in functions:
        result = f(result)
    return result

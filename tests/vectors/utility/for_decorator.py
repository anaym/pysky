def for_range(name, begin, end, step=1):
    def decorator(foo):
        def decorated(*args, **kwargs):
            if not kwargs:
                kwargs = {}
            results = []
            for i in range(begin, end, step):
                kwargs[name] = i
                results.append(foo(*args, **kwargs))
            return results
        return decorated
    return decorator

@for_range('i', 1, 100)
def foo(i):
    print(i)

# foo()
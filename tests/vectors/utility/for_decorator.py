def for_range(name, enum):
    def decorator(foo):
        def decorated(*args, **kwargs):
            if not kwargs:
                kwargs = {}
            results = []
            for i in enum:
                kwargs[name] = i
                results.append(foo(*args, **kwargs))
            return results
        return decorated
    return decorator


@for_range('i', range(0, 100))
def foo(i):
    print(i)

# foo()

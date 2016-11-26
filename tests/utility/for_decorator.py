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

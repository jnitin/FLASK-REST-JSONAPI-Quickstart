def ordered(obj):
    """Sorts a json dictionary, so we can do a compare.

    Recursively sort any lists it finds,
    and convert dictionaries to lists of (key, value) pairs,
    so that they're orderable.

    IMPORTANT: It returns a sorted list, not a json dict !

    Taken from:
    https://stackoverflow.com/questions/25851183/how-to-compare-two-json-objects-with-the-same-elements-in-a-different-order-equa  # NOQA
    """
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

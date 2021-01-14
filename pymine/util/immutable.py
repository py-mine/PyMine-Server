from immutables import Map


def make_immutable(obj: object) -> object:
    """Recursively converts lists to tuples and dictionaries to maps.

    :param object obj: A list or dict object.
    :return: Should be an immutable list or dict, or whatever else put in.
    :rtype: object
    """

    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = make_immutable(v)

        return Map(obj)

    if isinstance(obj, list):
        for i, v in enumerate(obj):
            obj[i] = make_immutable(v)

        return tuple(obj)

    return obj

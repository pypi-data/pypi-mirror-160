def flatten(to_flatten) -> list:
    flattened = []
    if isinstance(to_flatten, list):
        for item in to_flatten:
            flattened.extend(flatten(item))
    else:
        flattened.append(to_flatten)
    return flattened


def compact(l: list) -> list:
    return [item for item in l if item is not None]


def compact_dict(d: dict) -> dict:
    return {key: val for key, val in d.items() if val is not None}

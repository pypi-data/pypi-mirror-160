def valid(whatever) -> bool:
    if isinstance(whatever, str) and whatever.isdigit() and '.' not in whatever:
        return int(whatever) % 2 != 0
    elif isinstance(whatever, int):
        return whatever % 2 != 0
    raise ValueError('Invalid value')

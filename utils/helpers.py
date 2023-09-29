"""Various helper functions"""


def mask_string_value(value: str) -> str:
    """Masks given string value with * (to safely put into reports)"""
    size = len(value)
    if size < 2:
        value = value[-1:]
    elif size < 5:
        value = value[-2:]
    else:
        value = value[-3:]

    return f'****{value}'

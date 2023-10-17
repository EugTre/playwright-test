"""Various helper functions"""
import random
from copy import copy
from utils.models.admin_geozone import GeozoneEntity, CountryZoneEntity


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


def order_by_rules(items: list, ruleset: list, reverse: bool = False) -> list:
    """Sorts given list applying specific replacement rules.

    Args:
        items (list): list of items to sort.
        ruleset (list): list of pairs original value -
        equivalent for sorting.
        reverse (bool, optional): use reveresd sorting order.
        Defaults to False.

    Returns:
        list: sorted list.
    """
    sorted_items = copy(items)

    for find_what, replace_with in ruleset:
        idx = sorted_items.index(find_what)
        sorted_items[idx] = replace_with

    sorted_items.sort(reverse=reverse)
    for replace_with, find_what in ruleset:
        idx = sorted_items.index(find_what)
        sorted_items[idx] = replace_with

    return sorted_items


def generate_new_geozone_entity(
    add_countries: list[str] | tuple[str] | None = None
):
    """Creates Geozone entity with randomized name and
    some stub data.

    Args:
        add_countries (list[str] | tuple[str] | None, optional):
        list of countries value code to include"""
    geozone = GeozoneEntity(
        entity_id=None,
        code='TEST',
        name=f'Test-{random.randint(1000, 9999)}',
        description="Test Description Lines",
        zones=None
    )

    if not add_countries:
        return geozone

    geozone.zones = []
    for zone_value in add_countries:
        geozone.zones.append(
            CountryZoneEntity(
                zone_id=None,
                value=zone_value,
                city='Town'
            )
        )

    return geozone

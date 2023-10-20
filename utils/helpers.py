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


def compare_ordering(items: list, ruleset: list, assert_msg: str):
    """Sorts given list applying specific replacement rules,
    then checks that sorted and original lists are identical.

    Args:
        items (list): list of items to sort.
        ruleset (list): list of pairs original value -
        equivalent for sorting.
        assert_msg (str): assertion message.

    Raises:
        AssertionError: if order of items was changed
        after sorting.
    """
    sorted_items = copy(items)

    for find_what, replace_with in ruleset:
        if find_what in sorted_items:
            idx = sorted_items.index(find_what)
            sorted_items[idx] = replace_with

    sorted_items.sort(reverse=False)
    for replace_with, find_what in ruleset:
        if find_what in sorted_items:
            idx = sorted_items.index(find_what)
            sorted_items[idx] = replace_with

    assert items == sorted_items, assert_msg


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

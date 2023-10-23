"""Various helper functions"""
import random
from uuid import uuid4
from copy import copy

from utils.models.admin_geozone import CountryZoneEntity, GeozoneEntity
from utils.models.admin_product import ProductEntity


def mask_string_value(value: str) -> str:
    """Masks given string value with * (to safely put into reports)"""
    size = len(value)
    if size < 2:
        value = value[-1:]
    elif size < 5:
        value = value[-2:]
    else:
        value = value[-3:]

    return f"****{value}"


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
    add_countries: list[str] | tuple[str] | None = None,
):
    """Creates Geozone entity with randomized name and
    some stub data.

    Args:
        add_countries (list[str] | tuple[str] | None, optional):
        list of countries value code to include"""
    geozone = GeozoneEntity(
        entity_id=None,
        code="TEST",
        name=f"Test-{random.randint(1000, 9999)}",
        description="Test Description Lines",
        zones=None,
    )

    if not add_countries:
        return geozone

    geozone.zones = []
    for zone_value in add_countries:
        geozone.zones.append(
            CountryZoneEntity(zone_id=None, value=zone_value, city="Town")
        )

    return geozone


def generate_new_product_entity():
    """Creates instance of Product entity clas
    with randomized name and properties.
    """
    name_suffix = str(uuid4()).replace("-", " ")
    return ProductEntity(
        name=f"Pillow {name_suffix}",
        price=random.uniform(1.00, 1000.00),
        short_desc="Pokemon-themed pillow",
        full_desc="""
            Add a touch of cuteness and comfort to your home with this square
            Pikachu head-shaped pillow. Made with premium quality materials,
            this pillow is a must-have for any fan of the popular Pokémon
            franchise.

            Its vibrant yellow color and adorable facial features accurately
            depict the iconic character, creating a charming addition to any
            living space or bedroom. Whether you use it for decoration or for
            snuggling up during those cozy evenings, this Pikachu head pillow
            is sure to bring a smile to your face. Its soft and plush texture
            provides optimum comfort for relaxation and easily complements any
            interior style. Embrace the lovable world of Pikachu with this
            delightful square pillow that brings both charm and coziness to
            your home.
        """,
    )

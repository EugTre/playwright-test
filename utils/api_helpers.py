"""Collection of helpers to access API"""
import logging
from typing import Any
from collections.abc import Generator
from functools import cache

import allure
import requests

from utils.models.base_entity import BackOfficeEntity
from utils.models.entitiy_types import EntityType
from utils import helpers


GENERATOR_FUNCTIONS_PER_TYPE = {
    EntityType.GEOZONE: helpers.generate_new_geozone_entity,
    EntityType.PRODUCT: helpers.generate_new_product_entity
}

REQUESTS_PER_ENTITY_TYPE = {
    EntityType.GEOZONE: {
        "create": "/admin/?app=geo_zones&doc=edit_geo_zone",
        "delete":
            "/admin/?app=geo_zones&doc=edit_geo_zone&geo_zone_id={entity_id}",
    },
    EntityType.PRODUCT: {
        "create": "",
        "delete":
            "/admin/?app=catalog&doc=edit_product&category_id=0"
            "&product_id={entity_id}"
    }
}


@cache
def prepare_logged_admin_session(
    base_url: str, username: str, password: str
) -> requests.Session:
    """Logins using given creds and retun authorized session.

    Args:
        base_url (str): URL of API.
        username (str): username to use.
        password (str): password to use.

    Returns:
        requests.Session: authorized session.
    """
    session = requests.session()
    session.headers.update(
        {"Content-Type": "application/x-www-form-urlencoded"}
    )

    base_url = base_url.rstrip("/")
    session.post(
        f"{base_url}/admin/login.php",
        data="login=true&redirect_url=&login=Login"
        f"&username={username}&password={password}",
        allow_redirects=False,
        timeout=10,
    )

    return session


def create_admin_user(
    base_url: str, username: str, password: str
) -> tuple[str, str]:
    """Creates new admin user by API call"""
    new_username, new_password = helpers.generate_new_admin_user()

    session = prepare_logged_admin_session(
        base_url, username, password
    )

    session.post(
        f"{base_url}/admin/?app=users&doc=edit_user&page=1",
        data={
            "username": new_username,
            "password": new_password,
            "confirmed_password": new_password,
            "date_valid_from": "2023-09-20T00:00",
            "date_valid_to": "2025-09-20T00:00",
            "email": "",
            "status": "1",
            "save": "Save"
        },
        timeout=10,
    )

    return (new_username, new_password)


def create_entity_request(
    entity_type: EntityType,
    entity: BackOfficeEntity,
    session: requests.Session,
    base_url: str
) -> None:
    """API request to create new product from provided ProductEntity."""
    request_url = REQUESTS_PER_ENTITY_TYPE[entity_type]["create"]
    payload = entity.as_payload()

    session.post(
        f"{base_url}{request_url}",
        data={
            **payload,
            "save": "Save"
        },
        timeout=10,
    )


def get_new_entity(
    entity_type: EntityType,
    options: dict[str, Any],
    base_url: str,
    username: str,
    password: str,
) -> Generator[BackOfficeEntity, None, None]:
    """Creates entity of supported entity type using API
    request, returns entity to a fixture (and test),
    on teardown - deletes entity by another API call
    (if entity_id was reqtrieved from)

    Args:
        entity_type (EntityType): type of the entity to create.
        options (dict[str, Any]): options for entity generator.
        base_url (str): host of the API.
        username (str): admin username to use.
        password (str): admin password to user.

    Yields:
        _type_: _description_
    """

    logging.info("Creating new entity")
    entity_generator = GENERATOR_FUNCTIONS_PER_TYPE[entity_type]
    entity = entity_generator(**options)

    session = prepare_logged_admin_session(
        base_url, username, password
    )
    create_entity_request(entity_type, entity, session, base_url, )

    yield entity

    logging.info("On Teardown - deleting entity")
    delete_entity(entity, session, base_url)


def delete_entities(
    entities: list[BackOfficeEntity],
    base_url: str,
    username: str,
    password: str
) -> None:
    """Performs Delete request to API for given
    entities depending on entitity class"""
    session = prepare_logged_admin_session(
        base_url, username, password
    )

    for entity in entities:
        with allure.step(
            f"Sending API request to delete entity {entity}"
        ):
            delete_entity(entity, session, base_url)


def delete_entity(
    entity: BackOfficeEntity,
    session: requests.Session, base_url: str
):
    """Deletes entity using request selected by entity class"""
    request_url = REQUESTS_PER_ENTITY_TYPE[entity.entity_type]["delete"]
    request_url = request_url.format(entity_id=entity.entity_id)

    session.post(
        f"{base_url}{request_url}",
        data={"delete": "Delete"},
        timeout=10,
    )

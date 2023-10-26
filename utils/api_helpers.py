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
    EntityType.USER: helpers.generate_new_admin_user,
    EntityType.GEOZONE: helpers.generate_new_geozone_entity,
    EntityType.PRODUCT: helpers.generate_new_product_entity
}

REQUESTS_PER_ENTITY_TYPE = {
    EntityType.USER: {
        "create": {
            "url": "/admin/?app=users&doc=edit_user",
            "as_url_encoded": True
        },
        "delete": "/admin/?app=users&doc=edit_user&user_id={entity_id}"
    },
    EntityType.GEOZONE: {
        "create": {
            "url": "/admin/?app=geo_zones&doc=edit_geo_zone",
            "as_url_encoded": True
        },
        "delete":
            "/admin/?app=geo_zones&doc=edit_geo_zone&geo_zone_id={entity_id}",
    },
    EntityType.PRODUCT: {
        "create": {
            "url": "/admin/?category_id=0&app=catalog&doc=edit_product",
            "as_url_encoded": False
        },
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

    base_url = base_url.rstrip("/")
    session.post(
        f"{base_url}/admin/login.php",
        data={
            "redirect_url": "",
            "login": "Login",
            "username": username,
            "password": password
        },
        allow_redirects=False,
        timeout=10,
    )

    return session


def create_entity_request(
    entity_type: EntityType,
    entity: BackOfficeEntity,
    session: requests.Session,
    base_url: str
) -> None:
    """API request to create new product from provided ProductEntity."""
    request_url = REQUESTS_PER_ENTITY_TYPE[entity_type]["create"]["url"]
    as_url_encoded = \
        REQUESTS_PER_ENTITY_TYPE[entity_type]["create"]["as_url_encoded"]

    request_params = {
        "url": f"{base_url}{request_url}",
        "timeout": 10
    }

    if as_url_encoded:
        request_params["data"] = {
            **entity.as_payload(),
            "save": "Save"
        }
    else:
        request_params["files"] = {
            **entity.as_payload(),
            "save": (None, "Save")
        }

    response = session.post(**request_params)

    assert response.status_code == 200, \
        "Failed to create entity by API call. " \
        f"API returns code {response.status_code}."

    logging.info("Entity creation API call succeeded!")


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
        BackOfficeEntity: generated entity that was created on backend.
    """
    entity_generator = GENERATOR_FUNCTIONS_PER_TYPE[entity_type]
    if options is not None:
        entity = entity_generator(**options)
    else:
        entity = entity_generator()

    logging.info(
        "Creating new %s entity for test: %s",
        entity_type.value,
        entity
    )

    session = prepare_logged_admin_session(
        base_url, username, password
    )
    create_entity_request(entity_type, entity, session, base_url)

    yield entity

    logging.info("On Teardown: deleting entity %s", entity)
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
        logging.info("On Teardown: Deleting entity %s", entity)
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

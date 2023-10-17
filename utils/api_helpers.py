"""Collection of helpers to access API"""
import random
import requests

from utils.models.admin_geozone import GeozoneEntity


def prepare_logged_admin_session(base_url: str,
                                 username: str, password: str
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
    session.headers.update({
        "Content-Type": "application/x-www-form-urlencoded"
    })

    base_url = base_url.rstrip('/')
    session.post(
        f"{base_url}/admin/login.php",
        data='login=true&redirect_url=&login=Login'
             f'&username={username}&password={password}',
        allow_redirects=False,
        timeout=10
    )

    return session


def create_admin_user(session: requests.Session,
                      base_url: str) -> tuple[str, str]:
    """Creates new admin user by API call"""
    # Generate username and password
    username = ''.join((
        'admin_',
        str(random.randrange(1000, 9999)),
        str(random.randrange(1000, 9999))
    ))
    password = '_'.join((
        random.choice(["salty", "sweet", "sour", "mild", "spicy", "juicy"]),
        random.choice(["cookie", "pie", "beef", "soup", "salad", "porridge"])
    ))

    # Send API request to create new user
    session.post(
        f"{base_url}/admin/?app=users&doc=edit_user&page=1",
        data=f'username={username}&email='
             f'&password={password}&confirmed_password={password}'
             '&date_valid_from=2023-09-20T17%3A51'
             '&date_valid_to=2030-01-26T17%3A51&status=1&save=Save',
        timeout=10
    )

    return (username, password)


def create_empty_geo_zone(session: requests.Session, base_url: str,
                          geozone: GeozoneEntity) -> None:
    """API request to create new geozone with given geozone.code, geozone.name
    and geozone.desc, but with no countries attached"""
    body = (
        f'code={geozone.code}&name={geozone.name}'
        f'&description={geozone.description}'
        '&new_zone%5Bid%5D=&new_zone%5Bcountry_code%5D=&new_zone%5Bcity%5D='
        '&save=Save'
    )
    headers = {
        "Referer": f"{base_url}/admin/?app=geo_zones&doc=edit_geo_zone&page=1",
        "Upgrade-Insecure-Requests": "1"
    }
    session.post(
        url=f"{base_url}/admin/?app=geo_zones&doc=edit_geo_zone&page=1",
        data=body,
        headers=headers,
        timeout=10
    )


def delete_geo_zone(session: requests.Session, base_url: str,
                    geozone_id: int) -> None:
    """API request to delete geozone with given ID."""
    if geozone_id is None:
        return

    session.headers.update({
        "Referer": f"{base_url}/admin/?app=geo_zones&doc=edit_geo_zone&page=1"
                   f"&geo_zone_id={geozone_id}",
        "Upgrade-Insecure-Requests": "1"
    })

    session.post(
        f"{base_url}/admin/?app=geo_zones&doc=edit_geo_zone&page=1"
        f"&geo_zone_id={geozone_id}",
        data='code=&name=&description=&new_zone%5Bid%5D=&new_zone%5B'
             'country_code%5D=&new_zone%5Bcity%5D=&delete=Delete',
        timeout=10
    )

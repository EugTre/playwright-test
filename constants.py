"""Constants used by tests"""

# Leave empty if using --base-url CLI options
BASE_URL = 'http://192.168.56.104'

MESSAGES_REPOSITORY = 'resources/messages.ini'

# Admin user-pass for test environemnt
SUPERADMIN_USERNAME = "admin"
SUPERADMIN_PASSWORD = "secret"


COUNTRIES_ORDERING_RULES = [
    ('Åland Islands', 'Aland Islands'),
    ('Türkiye', 'Turkiye')
]

# Map of input fields to external links
COUNTRIES_FIELDS_ANNOTATION_LINKS = {
    'iso_code_1': (
        'Number (ISO 3166-1 numeric)',
        'https://en.wikipedia.org/wiki/ISO_3166-1_numeric',
    ),
    'iso_code_2': (
        'Code (ISO 3166-1 alpha-2)',
        'https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2'
    ),
    'iso_code_3': (
        'Code (ISO 3166-1 alpha-3)',
        'https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3'
    ),
    'address_format': (
        'Address Format (?)',
        'https://en.wikipedia.org/wiki/Address_(geography)'
    ),
    'tax_id_format': (
        'Tax ID Format',
        'https://en.wikipedia.org/wiki/Regular_expression'
    ),
    'postcode_format': (
        'Postcode Format ',
        'https://en.wikipedia.org/wiki/Regular_expression'
    ),
    'language_code': (
        'Language Code',
        'https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes'
    ),
    'currency_code': (
        'Currency Code',
        'https://en.wikipedia.org/wiki/'
        'List_of_countries_and_capitals_with_currency_and_language'
    ),
    'phone_code': (
        'Phone Country Code',
        'https://en.wikipedia.org/wiki/List_of_country_calling_codes'
    ),
}

# Product images for product creation
PRODUCT_IMAGES = [
    'resources/product.png'
]

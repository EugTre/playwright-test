# playwright-test

UI tests using Playwright / Pytest / Allure.

Repository contains:

- testing framework (page object models, components ad elements wrappers, api helper functions)
- tests related to admin backoffice of [Litecart](https://www.litecart.net/) e-shop

# <a name='toc'></a>Table of content
1. [Overview](#overview)
2. [How to use](#howto)
2. [Repository structure overview](#repo)

## <a name='overview'></a>Overview

Test suite applies to *Admin Backoffice* of the [Litecart](https://www.litecart.net/) e-shop.

Tests are made using BDD-like formatting and have highly detailed Allure reporting on each step/action taken. Each action/check also emits logs for debugging purposes. Tests are decorated with Allure epic/story/feature decorators, making reports more structured and readable.

Each test is isolated and ready to be run in separate process using `xdist` lib. Tests create and clean their test data using function scoped fixtures, leaving SUT in pretty the same state as before testing.

Suite is designed to use a *base url* for navigation, meaning that user must either specify `--base-url` CLI option or set `BASE_URL` constant at `constants.py` (CLI option will override constant if set).

Some tests are using visual comparison for page verification and/or uploaded image verification.

All tests track browser console errors and report occured errors both in logs and in Allure report.

## <a name='howto'></a>How to use

### Installation

1. Download Python 3.11+ (see https://www.python.org/downloads/)
2. Download and unpack project.
3. Navigate to project directory using terminal/cmd
4. Create virtual environment:
```cmd
python -m venv venv
```
5. Activate virtual environment:
```
# Windows
venv\Scripts\activate

# Linux
venv/bin/activate
```
6. Install dependencies:
```cmd
pip install -r requirements.txt
```
7. Install Allure commandline - see https://docs.qameta.io/allure/#_installing_a_commandline
8. Install Playwright browsers:
```
playwright install
```
9. Set up Litecart on your LAMP server, or build Docker image from https://github.com/EugTre/LAMP-Litecart-Docker
10. Set BASE_URL, SUPERADMIN_USERNAME and SUPERADMIN_PASSWORD in `constants.py`.

### Run tests

Default run options is set in `pytest.ini` file (pring logs, log levels,  and collect allure output).

To run tests it's enough to execute in terminal:
```
pytest tests -n auto
```

Show allure report:
```
allure server tmp
```

#### Command line options

**Playwright options:**
See [offical manual](https://playwright.dev/python/docs/test-runners#cli-arguments):

- `--base-url=<URL>` - sets base URL for tests.

- `--headed` - run tests in headed mode (with browser window displayed).

- `--browser <name>` - run test using given browser: chromium (default), firefox, webkit.

**Pytest / Allure options:**

- `-n auto` - to run test in parallel on several CPU cores (e.g. `-n 2` will run 2 processes).

- `--alluredir=tmp` - enables collection of Allure data to given directory.

- `--clean-alluredir` - cleans Allure dir from previous runs.

**Custom options:**

- `--maximized` - flag to maximize browser window/viewport to screen size.

- `--skip-snapshot-check` - flag to skip snapshot visual comparison (e.g. for faster debugging).

- `--snapshot-threshold=0.3` - threshold of snapshot visual comparison.  Defaults to 0.3.

#### pytest.ini options

- `log_cli = 1` and `log_level=<LEVEL>` - enables logging to termnial and set log level (DEBUG, INFO, WARN, ERROR, CRITICAL). By default only WARNING logs are captured.

- `allure.console_errors_to_step = true/false` - flag to save captured browser console errors as attachments to related Allure step. Defaults to True.


## <a name='repo'></a>Repository structure overview

### Project root

`conftest.py` contains pytest configuration and define basic fixtures to be used in tests.

`constants.py` - collection of static data used by tests.

`pytest.ini` - configuration file used by Pytest.

`setup.cfg` - project configuration type, used by Pylint and Flake.

### `resources` directory

Contains resources needed for tests (e.g. pictures for products).

`messages.ini` is a collection of texts used by test to compare against application. Used by `utils.text_repository.TextRepository` to extract message by it's key. Messages may be plain text or regex (should be wrapped with `r"..."` or `r'...'`).

### `tests` directory

Contains tests, grouped by tested components, and `conftest.py` file (stores various fixtures used test data generation and handling).

Some tests are using visual comparison for page verification. For such test there is `snapshot` directory exists next to test file which contains "golden" snapshot to compare with.

### `utils` directory

`api_helpers.py` provide functions to create/delete entities using API requests, used for test data creation.

`helpers.py` contains generator functions for test data creation and various helper functions to tests.

`bdd.py` provides 3 wrapper functions for Allure step with BDD-like names: `given`, `when`, `then`.

`text_repository.py` hosts a small class with only method `.get()`, that provides access to messages from `messages.ini` by string key in format `<section_name> <entry_name>`.

#### `components` directory

Describes common parts of the web pages and methods to interact with it (e.g. nav bars). Also describes elements compositions like Label + Input. Used by pages.

#### `elements` directory

Describes HTML elements, provides methods to interact and verify them. Used by pages and components.

#### `models` directory

Describes entities used in tests (e.g. product, user) and elements (table entry lookup/read strategy).

#### `pages` directory

Describes pages in Page Object Model approach, provides methods to interact and verify page content. Used in tests.

#### `steps` directory

Contains function that wraps some complex interaction or checks to make tests look cleaner and more constistent.

"""Small BDD-like context wrappers"""

import allure  # type: ignore


def given(title: str):
    """Allure step wrapper with 'Given xxx' title"""
    return allure.step(f"Given {title}")


def when(title: str):
    """Allure step wrapper with 'When xxx' title"""
    return allure.step(f"When {title}")


def then(title: str):
    """Allure step wrapper with 'Then xxx' title"""
    return allure.step(f"Then {title}")

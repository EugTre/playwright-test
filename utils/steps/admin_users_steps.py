import logging

from utils.models.admin_categories import AdminCategory
from utils.pages import AdminLoginPage, AdminUsersPage

from constants import SUPERADMIN_PASSWORD, SUPERADMIN_USERNAME


def find_user_exists(login_page: AdminLoginPage, entity):
    """Logins and navigates to Admin / Users page
    where tries to find given User entity"""

    logging.info("Find User Entity ID for %s", entity)
    login_page.visit()

    main_page = login_page.login(
        SUPERADMIN_USERNAME, SUPERADMIN_PASSWORD
    )
    users_page: AdminUsersPage = main_page.change_category(AdminCategory.USERS)
    users_page.find_in_table(entity, True)
    logging.info("Find User Entity ID for %s was done", entity)

    users_page.top_menu.log_out()

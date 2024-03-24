from http import HTTPStatus

from .helpers import (
    TestBaseClass,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    DELETE_SLUG_URL,
    EDIT_SLUG_URL,
    DETAIL_SLUG_URL,
    NOTES_HOME_URL,
    NOTES_LIST_URL,
    LOGIN_URL,
    SIGN_UP_URL,
    LOGOUT_URL,
    REDIRECT_URL
)

OK_STATUS = HTTPStatus.OK

NOT_FOUND_STATUS = HTTPStatus.NOT_FOUND


class TestRoutes(TestBaseClass):
    def test_availability_for_pages(self):
        parametrized_scenarios = (
            (DETAIL_SLUG_URL, self.auth_author, OK_STATUS),
            (DETAIL_SLUG_URL, self.auth_other_user, NOT_FOUND_STATUS),
            (EDIT_SLUG_URL, self.auth_author, OK_STATUS),
            (EDIT_SLUG_URL, self.auth_other_user, NOT_FOUND_STATUS),
            (DELETE_SLUG_URL, self.auth_author, OK_STATUS),
            (DELETE_SLUG_URL, self.auth_other_user, NOT_FOUND_STATUS),
            (NOTES_LIST_URL, self.auth_author, OK_STATUS),
            (NOTES_ADD_URL, self.auth_author, OK_STATUS),
            (NOTES_SUCCESS_URL, self.auth_author, OK_STATUS),
            (NOTES_HOME_URL, self.CLIENT, OK_STATUS),
            (LOGIN_URL, self.CLIENT, OK_STATUS),
            (LOGOUT_URL, self.CLIENT, OK_STATUS),
            (SIGN_UP_URL, self.CLIENT, OK_STATUS),
        )

        for url, user, status in parametrized_scenarios:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):

        parametrized_scenarios = (
            (EDIT_SLUG_URL, self.CLIENT),
            (DELETE_SLUG_URL, self.CLIENT),
            (DETAIL_SLUG_URL, self.CLIENT),
            (NOTES_LIST_URL, self.CLIENT),
            (NOTES_ADD_URL, self.CLIENT),
            (NOTES_SUCCESS_URL, self.CLIENT)
        )

        for url, user in parametrized_scenarios:
            final_url = REDIRECT_URL + url
            with self.subTest(url=url, user=user):
                self.assertRedirects(user.get(url), final_url)

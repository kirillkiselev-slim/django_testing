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
            (NOTES_HOME_URL, self.client, OK_STATUS),
            (LOGIN_URL, self.client, OK_STATUS),
            (LOGOUT_URL, self.client, OK_STATUS),
            (SIGN_UP_URL, self.client, OK_STATUS),
        )

        for url, user, status in parametrized_scenarios:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        parametrized_scenarios = (
            (EDIT_SLUG_URL, self.client),
            (DELETE_SLUG_URL, self.client),
            (DETAIL_SLUG_URL, self.client),
            (NOTES_LIST_URL, self.client),
            (NOTES_ADD_URL, self.client),
            (NOTES_SUCCESS_URL, self.client)
        )
        final_url_dict = {url: REDIRECT_URL + url for url, _ in parametrized_scenarios}

        for url, user in parametrized_scenarios:
            with self.subTest(url=url, user=user):
                self.assertRedirects(user.get(url), final_url_dict[url])

from http import HTTPStatus

from .base_class import TestBaseClass

OK_STATUS = HTTPStatus.OK

NOT_FOUND_STATUS = HTTPStatus.NOT_FOUND


class TestRoutes(TestBaseClass):
    def test_availability_for_pages(self):
        parametrized_scenarios = (
            (self.detail_slug, self.auth_author, OK_STATUS),
            (self.detail_slug, self.auth_other_user, NOT_FOUND_STATUS),
            (self.edit_slug, self.auth_author, OK_STATUS),
            (self.edit_slug, self.auth_other_user, NOT_FOUND_STATUS),
            (self.delete_slug, self.auth_author, OK_STATUS),
            (self.delete_slug, self.auth_other_user, NOT_FOUND_STATUS),
            (self.NOTES_LIST_URL, self.auth_author, OK_STATUS),
            (self.NOTES_ADD_URL, self.auth_author, OK_STATUS),
            (self.NOTES_SUCCESS_URL, self.auth_author, OK_STATUS),
            (self.NOTES_HOME_URL, self.CLIENT, OK_STATUS),
            (self.LOGIN_URL, self.CLIENT, OK_STATUS),
            (self.LOGOUT_URL, self.CLIENT, OK_STATUS),
            (self.SIGN_UP_URL, self.CLIENT, OK_STATUS),
        )

        for url, user, status in parametrized_scenarios:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        parametrized_scenarios = (
            (self.edit_slug, self.CLIENT),
            (self.delete_slug, self.CLIENT),
            (self.detail_slug, self.CLIENT),
            (self.NOTES_LIST_URL, self.CLIENT),
            (self.NOTES_ADD_URL, self.CLIENT),
            (self.NOTES_SUCCESS_URL, self.CLIENT)
        )

        for url, user in parametrized_scenarios:
            with self.subTest(url=url, user=user):
                self.assertRedirects(user.get(url), self.REDIRECT_URL + url)

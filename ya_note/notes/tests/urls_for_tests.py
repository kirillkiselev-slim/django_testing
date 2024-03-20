from django.urls import reverse

NOTES_HOME_URL = reverse('notes:home', None)

NOTES_LIST_URL = reverse('notes:list', None)

NOTES_ADD_URL = reverse('notes:add', None)

NOTES_SUCCESS_URL = reverse('notes:success', None)

SIGN_UP_URL = reverse('users:signup', None)

LOGIN_URL = reverse('users:login', None)

LOGOUT_URL = reverse('users:logout', None)


def detail_slug(note):
    return reverse('notes:detail', args=(note,))


def edit_slug(note):
    return reverse('notes:edit', args=(note,))


def delete_slug(note):
    return reverse('notes:delete', args=(note,))

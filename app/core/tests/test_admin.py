from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@gmail.com",
            password="adminpass"
        )
        self.client.force_login(self.admin_user)  # force_login() is helper function to prevent manual login
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password="userpass",
            name="ABC"
        )

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')  # app:url_we_want: generates url for list user page
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])    # generates /admin/core/user url
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

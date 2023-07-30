from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin.user",
            password="pwd12345"
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="test.user",
            password="userpwd123",
            years_of_experience=5
        )

    def test_redactor_years_of_experience_listed(self):
        url = reverse("admin:tracker_redactor_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.redactor.years_of_experience)

    def test_redactor_detailed_years_of_experience_listed(self):
        url = reverse("admin:tracker_redactor_change", args=[self.redactor.id])
        res = self.client.get(url)

        self.assertContains(res, self.redactor.years_of_experience)
        self.assertContains(res, self.redactor.first_name)
        self.assertContains(res, self.redactor.last_name)

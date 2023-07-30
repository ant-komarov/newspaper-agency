from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tracker.models import Topic, Redactor

TOPIC_LIST_URL = reverse("tracker:topic-list")
NEWSPAPER_LIST_URL = reverse("tracker:newspaper-list")
REDACTOR_LIST_URL = reverse("tracker:redactor-list")


class PublicViewsTest(TestCase):
    def test_login_required_topic_list_view(self):
        response = self.client.get(TOPIC_LIST_URL)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={TOPIC_LIST_URL}"
        )

    def test_login_required_newspaper_list_view(self):
        response = self.client.get(NEWSPAPER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={NEWSPAPER_LIST_URL}"
        )

    def test_login_required_redactor_list_view(self):
        response = self.client.get(REDACTOR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={REDACTOR_LIST_URL}"
        )


class PrivateTopicTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="pwd1234pwd",
            years_of_experience=9
        )
        self.client.force_login(self.user)

    def test_retrieve_topics(self):
        Topic.objects.create(name="Finance")
        Topic.objects.create(name="Art")

        response = self.client.get(TOPIC_LIST_URL)
        topics = Topic.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics)
        )
        self.assertTemplateUsed(
            response,
            "tracker/topic_list.html"
        )

    def test_retrieve_topics_search(self):
        search_param = "?name=o"
        topics_list = [
            "Culture",
            "Art",
            "Politics",
            "Technology",
            "Business",
            "Medicine"
        ]
        for item in topics_list:
            Topic.objects.create(name=item)

        response = self.client.get(TOPIC_LIST_URL + search_param)
        topics = Topic.objects.filter(name__icontains="o")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["topic_list"]),
            list(topics)
        )


class PrivateRedactorTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="pwd1234pwd",
            years_of_experience=9
        )
        self.client.force_login(self.user)

    def test_redactor_create_view(self):
        url = reverse("tracker:redactor-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/redactor_form.html")

    def test_redactor_create(self):
        url = reverse("tracker:redactor-create")
        form_data = {
            "username": "Test_user",
            "password1": "pwd12345pwd",
            "password2": "pwd12345pwd",
            "years_of_experience": 20
        }
        response = self.client.post(url, form_data)

        self.assertEqual(response.status_code, 302)

        redactor = get_user_model().objects.get(username="Test_user")

        self.assertEqual(redactor.years_of_experience, 20)

    def test_redactor_detail_view(self):
        redactor = Redactor.objects.create_user(
            username="test_user",
            password="pwd12345pwd",
            years_of_experience=15,
        )

        url = reverse("tracker:redactor-detail", args=[redactor.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/redactor_detail.html")
        self.assertContains(response, "test_user")


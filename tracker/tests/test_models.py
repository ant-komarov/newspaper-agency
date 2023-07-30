from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from tracker.models import Topic, Newspaper


class ModelsTest(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="Sport")

        self.assertEqual(str(topic), topic.name)

    def test_newspaper_str(self):
        topic = Topic.objects.create(name="IT")
        newspaper = Newspaper.objects.create(
            title="Test",
            content="test content",
            publish_date=datetime.now().date(),
            topic=topic
        )

        self.assertEqual(
            str(newspaper),
            f"{newspaper.title}, published {newspaper.publish_date}"
        )

    def test_create_redactor_with_yeas_of_experience(self):
        username = "test_user"
        password = "pwd12345pwd"
        years_of_experience = 15

        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEqual(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEqual(redactor.years_of_experience, years_of_experience)

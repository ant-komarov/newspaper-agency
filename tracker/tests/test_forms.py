from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from tracker.forms import RedactorCreationForm, NewspaperForm


class RedactorFormTest(TestCase):
    def test_redactor_creation_with_first_last_name_years_of_experience_valid(self):
        form_data = {
            "username": "redactor",
            "password1": "pwd12345pwd",
            "password2": "pwd12345pwd",
            "first_name": "Tester",
            "last_name": "Testenko",
            "years_of_experience": 10
        }
        form = RedactorCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_redactor_creation_with_years_of_experience_invalid(self):
        form_data = {
            "username": "redactor",
            "password1": "pwd12345pwd",
            "password2": "pwd12345pwd",
            "first_name": "Tester",
            "last_name": "Testenko",
            "years_of_experience": -1
        }

        form = RedactorCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            "Years of experience must be greater or equal 0"
        )


class NewspaperFormTest(TestCase):
    def test_create_newspaper_publish_date_invalid(self):
        form_data = {
            "title": "Test title",
            "content": "Test content",
            "publish_date": datetime.now().date() + timedelta(days=1),
            "publishers": []
        }

        form = NewspaperForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            ValidationError,
            "Newspaper can't be published in future!!!"
        )


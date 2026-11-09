"""Additional Part 2 regression tests for URL and form behaviour."""

from django.test import TestCase
from django.urls import resolve, reverse

from .models import Note


class PartTwoRegressionTests(TestCase):
    def test_named_routes_resolve_to_expected_views(self):
        for name in ["list", "create", "detail", "update", "delete"]:
            with self.subTest(name=name):
                args = [] if name in {"list", "create"} else [7]
                match = resolve(reverse(f"notes:{name}", args=args))
                self.assertEqual(match.view_name, f"notes:{name}")

    def test_successful_create_shows_confirmation_after_redirect(self):
        response = self.client.post(reverse("notes:create"), {
            "title": "Read lesson", "content": "Practise testing",
        }, follow=True)
        self.assertContains(response, "Your note has been saved.")
        self.assertContains(response, "Practise testing")

    def test_boundary_length_title_is_accepted(self):
        response = self.client.post(reverse("notes:create"), {
            "title": "x" * 200, "content": "Valid content",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Note.objects.get().title), 200)

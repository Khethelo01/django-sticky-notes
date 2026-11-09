"""Verify note CRUD, validation, HTTP safety and template rendering."""

from django.contrib.staticfiles import finders
from django.test import Client, TestCase
from django.urls import reverse

from .forms import NoteForm
from .models import Note


class NoteTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(title="Remember", content="Study MVT")
        self.detail = reverse("notes:detail", args=[self.note.pk])
        self.update = reverse("notes:update", args=[self.note.pk])
        self.delete = reverse("notes:delete", args=[self.note.pk])

    def test_model_string_and_timestamps(self):
        self.assertEqual(str(self.note), "Remember")
        self.assertIsNotNone(self.note.created_at)
        self.assertIsNotNone(self.note.updated_at)
        self.assertEqual(self.note.get_absolute_url(), self.detail)

    def test_list_renders_notes_and_base_template(self):
        response = self.client.get(reverse("notes:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "notes/note_list.html")
        self.assertContains(response, "Remember")
        self.assertContains(response, "/static/notes/styles.css")

    def test_empty_board_explains_how_to_start(self):
        Note.objects.all().delete()
        response = self.client.get(reverse("notes:list"))
        self.assertContains(response, "Write your first note")

    def test_detail_shows_full_content(self):
        response = self.client.get(self.detail)
        self.assertContains(response, "Study MVT")
        self.assertContains(response, "Edit note")

    def test_create_saves_and_redirects_to_detail(self):
        response = self.client.post(reverse("notes:create"), {
            "title": " New note ", "content": "Some useful content",
        })
        note = Note.objects.get(title="New note")
        self.assertRedirects(response, note.get_absolute_url())
        self.assertEqual(note.content, "Some useful content")
        self.assertEqual(Note.objects.count(), 2)

    def test_create_get_does_not_save(self):
        response = self.client.get(reverse("notes:create"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)

    def test_invalid_create_displays_errors_and_keeps_input(self):
        response = self.client.post(reverse("notes:create"), {
            "title": "  ", "content": "Keep this draft",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertContains(response, "Keep this draft")
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_post_is_bound_and_rejected(self):
        response = self.client.post(reverse("notes:create"), {})
        self.assertTrue(response.context["form"].is_bound)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Note.objects.count(), 1)

    def test_form_rejects_missing_content_and_long_title(self):
        for data in [
            {"title": "Title", "content": "  "},
            {"title": "a" * 201, "content": "Content"},
        ]:
            with self.subTest(data=data):
                self.assertFalse(NoteForm(data=data).is_valid())

    def test_update_get_prefills_form(self):
        response = self.client.get(self.update)
        self.assertEqual(response.context["form"].instance, self.note)
        self.assertContains(response, "Study MVT")

    def test_update_persists_and_preserves_creation_time(self):
        original_created = self.note.created_at
        original_updated = self.note.updated_at
        response = self.client.post(self.update, {
            "title": "Revised", "content": "Revised text",
        })
        self.assertRedirects(response, self.detail)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Revised")
        self.assertEqual(self.note.content, "Revised text")
        self.assertEqual(self.note.created_at, original_created)
        self.assertGreaterEqual(self.note.updated_at, original_updated)
        self.assertEqual(Note.objects.count(), 1)

    def test_invalid_update_preserves_saved_note(self):
        response = self.client.post(self.update, {
            "title": "", "content": "Changed",
        })
        self.assertTrue(response.context["form"].errors)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Remember")
        self.assertEqual(self.note.content, "Study MVT")

    def test_delete_get_only_displays_confirmation(self):
        response = self.client.get(self.delete)
        self.assertContains(response, "Delete this note?")
        self.assertContains(response, "Keep note")
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_delete_post_removes_only_selected_note(self):
        other = Note.objects.create(title="Keep", content="Keep me")
        response = self.client.post(self.delete)
        self.assertRedirects(response, reverse("notes:list"))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
        self.assertTrue(Note.objects.filter(pk=other.pk).exists())

    def test_missing_notes_return_404(self):
        for name in ["detail", "update", "delete"]:
            with self.subTest(name=name):
                url = reverse(f"notes:{name}", args=[99999])
                self.assertEqual(self.client.get(url).status_code, 404)

    def test_html_is_escaped_when_displayed(self):
        self.note.content = "<script>alert('unsafe')</script>"
        self.note.save()
        response = self.client.get(self.detail)
        self.assertNotContains(response, "<script>")
        self.assertContains(response, "&lt;script&gt;")

    def test_csrf_protects_create_update_and_delete(self):
        client = Client(enforce_csrf_checks=True)
        for url in [reverse("notes:create"), self.update, self.delete]:
            with self.subTest(url=url):
                self.assertEqual(client.post(url, {}).status_code, 403)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_unsupported_http_methods_are_rejected(self):
        self.assertEqual(self.client.put(self.delete).status_code, 405)
        self.assertEqual(
            self.client.post(reverse("notes:list")).status_code, 405
        )

    def test_css_is_discovered(self):
        self.assertIsNotNone(finders.find("notes/styles.css"))

from django.test import TestCase
from django.urls import reverse

from .models import Note


class NotePagesTests(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="Тестовая заметка",
            content="Текст заметки",
        )

    def test_list_displays_note(self):
        response = self.client.get(reverse("notes:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)

    def test_create_note(self):
        response = self.client.post(
            reverse("notes:create"),
            {
                "title": "Новая заметка",
                "content": "Содержание новой заметки",
            },
        )

        self.assertRedirects(response, reverse("notes:list"))
        self.assertTrue(
            Note.objects.filter(title="Новая заметка").exists()
        )

    def test_update_note(self):
        response = self.client.post(
            reverse("notes:update", kwargs={"pk": self.note.pk}),
            {
                "title": "Изменённая заметка",
                "content": "Обновлённый текст",
            },
        )

        self.assertRedirects(response, reverse("notes:list"))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Изменённая заметка")
        self.assertEqual(self.note.content, "Обновлённый текст")

    def test_delete_note(self):
        response = self.client.post(
            reverse("notes:delete", kwargs={"pk": self.note.pk})
        )

        self.assertRedirects(response, reverse("notes:list"))
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_list_uses_two_queries(self):
        with self.assertNumQueries(2):
            response = self.client.get(reverse("notes:list"))

        self.assertEqual(response.status_code, 200)

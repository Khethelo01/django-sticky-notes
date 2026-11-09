"""Persistent sticky note entity."""

from django.db import models
from django.urls import reverse


class Note(models.Model):
    """Store a note's title, content and automatic timestamps."""

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-pk"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("notes:detail", kwargs={"pk": self.pk})

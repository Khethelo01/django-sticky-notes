"""Shared form validation for creating and updating notes."""

from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """Expose only editable note fields with server-side validation."""

    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Give your note a title",
                "autofocus": True,
            }),
            "content": forms.Textarea(attrs={
                "rows": 8,
                "placeholder": "Write what you want to remember...",
            }),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Please enter a title.")
        return title

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if not content:
            raise forms.ValidationError("Please write some note content.")
        return content

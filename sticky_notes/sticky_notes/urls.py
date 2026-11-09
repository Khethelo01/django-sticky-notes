"""Include the notes application's routes at the site root."""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("notes.urls")),
]

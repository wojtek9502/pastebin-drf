from django.urls import path

from .views import NoteCreateAPIView, NoteDetailAPIView

urlpatterns = [
    path("note", NoteCreateAPIView.as_view()),
    path("note/<slug:slug>", NoteDetailAPIView.as_view()),
]

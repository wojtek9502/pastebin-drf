from django.urls import path

from .views import NoteCreateAPIView, NoteDetailAPIView, NoteListAPIView, NoteDetailByIdAPIView

urlpatterns = [
    path("note", NoteCreateAPIView.as_view()),
    path("note/all", NoteListAPIView.as_view()),
    path("note/<uuid:id>", NoteDetailByIdAPIView.as_view()),
    path("note/<slug:link_slug>", NoteDetailAPIView.as_view()),
]

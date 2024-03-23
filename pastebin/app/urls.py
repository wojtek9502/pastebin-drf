from django.urls import path

from .views import NoteCreateAPIView, NoteDetailBySlugAPIView, NoteListAPIView, NoteDetailByIdAPIView, \
    NoteListPublicLatestAPIView, HealthzAPIView, NoteIsPasswordNeededAPIView, NoteDeleteAPIView, \
    NodePasswordProtectedDetailByIdAPIView, NodePasswordProtectedDetailByLinkSlugAPIView

urlpatterns = [
    path("note/", NoteCreateAPIView.as_view()),
    path("note/all", NoteListAPIView.as_view()),
    path("note/public/latest", NoteListPublicLatestAPIView.as_view()),
    path("note/<uuid:id>", NoteDetailByIdAPIView.as_view()),
    path("note/secured/by_id", NodePasswordProtectedDetailByIdAPIView.as_view()),
    path("note/secured/by_link", NodePasswordProtectedDetailByLinkSlugAPIView.as_view()),
    path("note/<slug:link_slug>", NoteDetailBySlugAPIView.as_view()),
    path("note/<slug:link_slug>/is_password_needed", NoteIsPasswordNeededAPIView.as_view()),
    path("note/<slug:link_slug>/delete", NoteDeleteAPIView.as_view()),

    path("healthz", HealthzAPIView.as_view()),
]

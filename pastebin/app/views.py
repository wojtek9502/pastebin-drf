from .models import NoteModel
from .serializers import NoteSerializer
from rest_framework import generics


class NoteCreateAPIView(generics.CreateAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'slug'


class NoteDetailAPIView(generics.RetrieveAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'slug'

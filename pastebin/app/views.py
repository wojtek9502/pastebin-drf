from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import NoteModel
from .serializers import NoteSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from .services import NoteService
from .utils.helpers import validate_serializer
from .utils.models_choices import NoteExposureChoices, NoteExpirationChoices
from .pagination import PaginationClass


class NoteCreateAPIView(generics.CreateAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'link_slug'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        validate_serializer(serializer)
        serializer_data = serializer.data

        # create note
        data = request.data
        service = NoteService()
        note_instance = service.create_note(note_data=data)

        # return API response
        response_data = serializer_data
        response_data['id'] = note_instance.id
        response_data['link_slug'] = note_instance.link_slug
        return Response(serializer_data, status=status.HTTP_201_CREATED)


class NoteListPublicLatestAPIView(generics.ListAPIView):
    queryset = NoteModel.objects.filter(
        Q(exposure_type=NoteExposureChoices.PUBLIC) &
        ~Q(expiration_type=NoteExpirationChoices.BURN_AFTER_READ)
    ).order_by('-inserted_on')[:10]

    serializer_class = NoteSerializer
    lookup_field = 'link_slug'


class NoteDetailBySlugAPIView(generics.RetrieveAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'link_slug'


class NoteDetailByIdAPIView(generics.RetrieveAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'id'


class NoteListAPIView(generics.ListAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'link_slug'
    pagination_class = PaginationClass


class NoteDeleteAPIView(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    lookup_field = 'link_slug'

    def get_queryset(self):
        queryset = NoteModel.objects.filter(link_slug=self.kwargs['link_slug'])
        return queryset


class NoteIsPasswordNeededAPIView(APIView):
    def get(self, request, link_slug: str, format=None):
        instance_data = NoteModel.objects.values_list('is_password').get(link_slug=link_slug)
        if not instance_data:
            raise ValidationError("Note not exists")

        response_data = dict(is_password_needed=instance_data[0])
        return Response(response_data)


class HealthzAPIView(APIView):
    def get(self, request, format=None):
        response_data = dict(status="OK")
        return Response(response_data)

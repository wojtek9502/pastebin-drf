from uuid import UUID

from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import NoteModel
from .serializers import NoteSerializer, NoteFetchByIdSerializer, NoteFetchByLinkSlugSerializer
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


class NodePasswordProtectedDetailByIdAPIView(APIView):
    @extend_schema(
        request=NoteFetchByIdSerializer,
        responses=NoteSerializer
    )
    def post(self, request, format=None):
        node_instance = NoteService().fetch_password_protected_note_by_id(
            note_id=UUID(request.data['id']),
            password_user_input=request.data['password_clear']
        )
        if not node_instance:
            return Response("Note not found or bad password", status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(node_instance)
        return Response(serializer.data)


class NodePasswordProtectedDetailByLinkSlugAPIView(APIView):
    @extend_schema(
        request=NoteFetchByLinkSlugSerializer,
        responses=NoteSerializer
    )
    def post(self, request, format=None):
        node_instance = NoteService().fetch_password_protected_note_by_link_slug(
            link_slug=request.data['link_slug'],
            password_user_input=request.data['password_clear']
        )
        if not node_instance:
            return Response("Note not found or bad password", status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(node_instance)
        return Response(serializer.data)


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
    def post(self, request, format=None):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthzAPIView(APIView):
    def get(self, request, format=None):
        response_data = dict(status="OK")
        return Response(response_data)

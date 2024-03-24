from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView

from .models import NoteModel
from .serializers import NoteSerializer, NoteFetchByIdSerializer, NoteFetchByLinkSlugSerializer, \
    NodeIsPasswordNeededSerializer, HealthzSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from .services import NoteService
from .utils.compression import NoteCompressionService
from .utils.models_choices import NoteExposureChoices, NoteExpirationChoices
from .pagination import PaginationClass
from django.forms.models import model_to_dict


class NoteCreateAPIView(generics.CreateAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'link_slug'

    def create(self, request, *args, **kwargs):
        # create note
        data = request.data
        service = NoteService()
        note_instance = service.create_note(note_data=data)

        # return API response
        response_data = model_to_dict(note_instance)
        response_data['text'] = NoteCompressionService.decompress(bytes(note_instance.text))
        response_data['inserted_on'] = str(note_instance.inserted_on)
        response_data['updated_on'] = str(note_instance.inserted_on)
        del response_data['password']
        return Response(response_data, status=status.HTTP_201_CREATED)


class NoteListPublicLatestAPIView(generics.ListAPIView):
    queryset = NoteModel.objects.filter(
        Q(exposure_type=NoteExposureChoices.PUBLIC) &
        ~Q(expiration_type=NoteExpirationChoices.BURN_AFTER_READ)
    ).order_by('-inserted_on')[:10]

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
    serializer_class = NodeIsPasswordNeededSerializer

    def get(self, request, link_slug: str, format=None):
        try:
            note_instance = NoteModel.objects.get(link_slug=link_slug)
        except ObjectDoesNotExist:
            return Response("Note not found", status=status.HTTP_404_NOT_FOUND)

        return Response(dict(is_password=note_instance.is_password))


class HealthzAPIView(APIView):
    serializer_class = HealthzSerializer

    def get(self, request, format=None):
        response_data = dict(status="OK")
        return Response(response_data)

from .models import NoteModel, TagModel, CategoryModel
from .serializers import NoteSerializer
from rest_framework import generics, status
from rest_framework.response import Response

from .utils.helpers import get_note_link_slug


class NoteCreateAPIView(generics.CreateAPIView):
    queryset = NoteModel.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'link_slug'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer_data = serializer.data
        serializer.validate(data=serializer_data)

        data = request.data
        tags = data['tags']
        categories = data['categories']

        # create note instance
        note_instance = NoteModel.objects.create(
            title=data['title'],
            text=data['text'],
            link_slug=get_note_link_slug(),
            expiration_type=data['expiration_type'],
            exposure_type=data['exposure_type'],
            syntax=data['syntax'],
            is_password=data['is_password']
        )
        note_instance.save()

        # create tags
        tags_instances = []
        for tag_name in tags:
            tag_instance, is_created = TagModel.objects.get_or_create(name=tag_name)
            tags_instances.append(tag_instance)

        # create categories
        categories_instances = []
        for category_name in categories:
            category_instance, is_created = CategoryModel.objects.get_or_create(name=category_name)
            categories_instances.append(category_instance)

        # add many to many instances to note instance
        note_instance.tags.set(tags_instances)
        note_instance.categories.set(categories_instances)

        # return API response
        response_data = serializer_data
        response_data['id'] = note_instance.id
        response_data['link_slug'] = note_instance.link_slug
        return Response(serializer_data, status=status.HTTP_201_CREATED)


class NoteDetailAPIView(generics.RetrieveAPIView):
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

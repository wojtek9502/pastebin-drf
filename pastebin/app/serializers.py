from hashlib import sha256

from . import models
from rest_framework import serializers
from rest_framework.fields import CharField


from .utils.models_choices import NoteExpirationChoices, NoteExposureChoices, NoteSyntaxChoices


class CategorySerializer(serializers.ModelSerializer):
    name = CharField( required=True)

    class Meta:
        model = models.CategoryModel
        fields = ('name',)


class TagSerializer(serializers.ModelSerializer):
    name = CharField(required=True)

    class Meta:
        model = models.CategoryModel
        fields = ('name',)


class NoteSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format='hex', read_only=True)
    title = CharField(required=True)
    text = CharField(required=True)
    expiration_type = CharField(required=False, default=NoteExpirationChoices.NEVER)
    exposure_type = CharField(required=False, default=NoteExposureChoices.PUBLIC)
    syntax = CharField(required=False, default=NoteSyntaxChoices.NONE)
    is_password = CharField(required=False, default=True)
    link_slug = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    def get_link_slug(self, instance):
        id_str = str(instance.id)
        return sha256(id_str.encode('utf-8')).hexdigest()

    class Meta:
        model = models.NoteModel
        fields = '__all__'

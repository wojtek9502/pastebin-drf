from . import models
from rest_framework import serializers
from rest_framework.fields import CharField, DateTimeField, BooleanField

from .utils.models_choices import NoteExpirationChoices, NoteExposureChoices, NoteSyntaxChoices


class NoteFetchByIdSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    password_clear = CharField(default='', required=False)


class NoteFetchByLinkSlugSerializer(serializers.Serializer):
    link_slug = CharField(required=True)
    password_clear = CharField(default='', required=False)


class CategorySerializer(serializers.ModelSerializer):
    name = CharField(default='')

    class Meta:
        model = models.CategoryModel
        fields = ('name',)


class TagSerializer(serializers.ModelSerializer):
    name = CharField(default='')

    class Meta:
        model = models.CategoryModel
        fields = ('name',)


class NoteSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    title = CharField(required=True)
    text = CharField(required=True)
    link_slug = CharField(read_only=True)
    expiration_type = CharField(required=False, default=NoteExpirationChoices.NEVER)
    exposure_type = CharField(required=False, default=NoteExposureChoices.PUBLIC)
    syntax = CharField(required=False, default=NoteSyntaxChoices.NONE)
    password_clear = CharField(source='password', required=False, write_only=True, default='')
    is_password = BooleanField(read_only=True, default=False)
    categories = CategorySerializer(many=True, default=[])
    tags = TagSerializer(many=True, default=[])
    inserted_on = DateTimeField(read_only=True)
    updated_on = DateTimeField(read_only=True)

    class Meta:
        model = models.NoteModel
        fields = ('id', 'title', 'text', 'link_slug', 'expiration_type',
                  'exposure_type', 'syntax', 'password_clear', 'is_password',
                  'categories', 'tags', 'inserted_on', 'updated_on')

    def validate(self, data):
        expiration_type = data["expiration_type"]
        expiration_type_choices = [choice[0] for choice in NoteExpirationChoices.choices]
        if not (expiration_type in expiration_type_choices):
            raise serializers.ValidationError(
                {"Invalid Choice": f"expiration_type field is not valid. Valid choices {expiration_type_choices}"})

        exposure_type = data["exposure_type"]
        exposure_type_choices = [choice[0] for choice in NoteExposureChoices.choices]
        if not (exposure_type in exposure_type_choices):
            raise serializers.ValidationError(
                {"Invalid Choice": f"exposure_type field is not valid. Valid choices {exposure_type_choices}"})

        syntax = data["syntax"]
        syntax_choices = [choice[0] for choice in NoteSyntaxChoices.choices]
        if not (syntax in syntax_choices):
            raise serializers.ValidationError(
                {"Invalid Choice": f"syntax field is not valid. Valid choices {syntax_choices}"})

        return data

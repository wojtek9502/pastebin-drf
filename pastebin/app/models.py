from django.db import models

from .utils.models_abstractions import BaseModel, InsertedOnModel, UpdatedOnModel
from .utils.models_choices import NoteSyntaxChoices, NoteExposureChoices, NoteExpirationChoices, \
    NoteCategoryChoices


# Create your models here.
class CategoryModel(BaseModel, InsertedOnModel, UpdatedOnModel):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, choices=NoteCategoryChoices.choices)

    def __str__(self):
        return f'id: {self.id}, category: {self.name}'


class TagModel(BaseModel, InsertedOnModel, UpdatedOnModel):
    class Meta:
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=100, choices=NoteCategoryChoices.choices)

    def __str__(self):
        return f'id: {self.id}, tag: {self.name}'


class NoteModel(BaseModel, InsertedOnModel, UpdatedOnModel):
    class Meta:
        verbose_name_plural = "Notes"

    title = models.CharField(1024)
    text = models.TextField()
    expiration_type = models.CharField(max_length=50, choices=NoteExpirationChoices.choices)
    exposure_type = models.CharField(max_length=50, choices=NoteExposureChoices.choices)
    syntax = models.CharField(max_length=50, choices=NoteSyntaxChoices.choices)
    is_password = models.BooleanField()
    link_slug = models.SlugField(max_length=120)
    categories = models.ManyToManyField(CategoryModel, related_name="categories")
    tags = models.ManyToManyField(TagModel, related_name="tags")

    def __str__(self):
        return f'id {self.id}, title: {self.title}, is_password: {self.is_password}'

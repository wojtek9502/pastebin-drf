from django.db import models

from .utils.models_abstractions import BaseModel
from .utils.models_choices import NoteSyntaxChoices, NoteExposureChoices, NoteExpirationChoices, \
    NoteCategoryChoices


# Create your models here.
class CategoryModel(BaseModel):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, choices=NoteCategoryChoices.choices)

    def __str__(self):
        return f'id: {self.id}, category: {self.name}'


class TagModel(BaseModel):
    class Meta:
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=100, choices=NoteCategoryChoices.choices)

    def __str__(self):
        return f'id: {self.id}, tag: {self.name}'


class NotePasswordModel(BaseModel):
    password_hash = models.BinaryField()
    salt = models.BinaryField()
    iterations = models.IntegerField(default=100_000)


class NoteModel(BaseModel):
    class Meta:
        verbose_name_plural = "Notes"

    title = models.CharField(1024)
    text = models.BinaryField()
    link_slug = models.SlugField(max_length=120)
    expiration_type = models.CharField(max_length=50, choices=NoteExpirationChoices.choices, default=NoteExpirationChoices.NEVER)
    expiration_date = models.DateTimeField(null=True)
    exposure_type = models.CharField(max_length=50, choices=NoteExposureChoices.choices, default=NoteExposureChoices.PUBLIC)
    syntax = models.CharField(max_length=50, choices=NoteSyntaxChoices.choices, default=NoteSyntaxChoices.NONE)
    password = models.OneToOneField(NotePasswordModel, on_delete=models.CASCADE, null=True)
    is_password = models.BooleanField(default=False)

    categories = models.ManyToManyField(CategoryModel, related_name="categories")
    tags = models.ManyToManyField(TagModel, related_name="tags")


    def __str__(self):
        return f'id {self.id}, title: {self.title}, is_password: {self.is_password}'

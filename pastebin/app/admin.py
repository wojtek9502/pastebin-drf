from django.contrib import admin
from .models import NoteModel, CategoryModel, TagModel


@admin.register(NoteModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'expiration_type', 'exposure_type', 'syntax', 'is_password', 'link_slug')


@admin.register(CategoryModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(TagModel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

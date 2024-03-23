from typing import Dict

from .models import NoteModel, TagModel, CategoryModel
from .utils.helpers import get_note_link_slug


class NoteService:
    def create_note(self, note_data: Dict) -> NoteModel:
        tags = note_data['tags']
        categories = note_data['categories']

        # create note instance
        note_instance = NoteModel.objects.create(
            title=note_data['title'],
            text=note_data['text'],
            link_slug=get_note_link_slug(),
            expiration_type=note_data['expiration_type'],
            exposure_type=note_data['exposure_type'],
            syntax=note_data['syntax'],
            is_password=note_data['is_password']
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

        return note_instance

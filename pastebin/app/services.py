import os
from typing import Dict
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from .models import NoteModel, TagModel, CategoryModel, NotePasswordModel
from .utils.cryptography import PasswordHashService, PasswordHashDTO
from .utils.helpers import get_note_link_slug


class NoteService:
    @staticmethod
    def _create_password_hash(password_clear: str, iterations: int = None, salt: bytes = None) -> PasswordHashDTO:
        hash_dto = PasswordHashService().create_hash(
            password_clear=password_clear,
            iterations=iterations,
            salt=salt
        )
        return hash_dto

    def _is_password_valid(self, password_user_input: str, password_db_instance: NotePasswordModel) -> bool:
        password_salt = bytes(password_db_instance.salt)
        password_iterations = password_db_instance.iterations
        password_from_db_hash = bytes(password_db_instance.password_hash)

        password_user_input = self._create_password_hash(
            password_clear=password_user_input,
            iterations=password_iterations,
            salt=password_salt
        )

        return password_user_input.password_hash == password_from_db_hash

    def create_note(self, note_data: Dict) -> NoteModel:
        tags = note_data['tags']
        categories = note_data['categories']
        password = note_data['password_clear']
        is_password = True if len(password) else False

        # create password
        password_instance = None
        if len(password):
            password_hash = self._create_password_hash(password_clear=password)
            password_instance = NotePasswordModel.objects.create(
                password_hash=password_hash.password_hash,
                salt=password_hash.salt,
                iterations=int(os.environ['NOTE_PASSWORDS_HASH_N_ITERATIONS'])
            )

        # create note instance
        note_instance = NoteModel.objects.create(
            title=note_data['title'],
            text=note_data['text'],
            link_slug=get_note_link_slug(),
            expiration_type=note_data['expiration_type'],
            exposure_type=note_data['exposure_type'],
            syntax=note_data['syntax'],
            password=password_instance,
            is_password=is_password
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

    def fetch_password_protected_note_by_id(self, note_id: UUID, password_user_input: str):
        try:
            note_instance = NoteModel.objects.get(id=note_id)
        except ObjectDoesNotExist as e:
            note_instance = None

        if note_instance:
            is_password_valid = self._is_password_valid(
                password_db_instance=note_instance.password,
                password_user_input=password_user_input
            )
            if is_password_valid:
                return note_instance
        return None

    def fetch_password_protected_note_by_link_slug(self, link_slug: str, password_user_input: str):
        try:
            note_instance = NoteModel.objects.get(link_slug=link_slug)
        except ObjectDoesNotExist as e:
            note_instance = None

        if note_instance:
            is_password_valid = self._is_password_valid(
                password_db_instance=note_instance.password,
                password_user_input=password_user_input
            )
            if is_password_valid:
                return note_instance
        return None

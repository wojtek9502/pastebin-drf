import datetime
import logging
import os
from typing import Dict, Optional
from uuid import UUID

from pytz import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.timezone import get_current_timezone
from dateutil.relativedelta import *


from .models import NoteModel, TagModel, CategoryModel, NotePasswordModel
from .utils.compression import NoteCompressionService
from .utils.cryptography import PasswordHashService, PasswordHashDTO
from .utils.helpers import get_note_link_slug
from .utils.models_choices import NoteExpirationChoices

logger = logging.getLogger(__name__)


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
        note_compressed = NoteCompressionService.compress(note_data['text_input'])
        expiration_date = NoteExpirationService.calc_expiration_date(
            expiration_type=NoteExpirationChoices(note_data['expiration_type'])
        )

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
            text=note_compressed,
            link_slug=get_note_link_slug(),
            expiration_type=note_data['expiration_type'],
            expiration_date=expiration_date,
            exposure_type=note_data['exposure_type'],
            syntax=note_data['syntax'],
            password=password_instance,
            is_password=is_password,
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

    def process_note(self, note_instance: NoteModel, password: str) -> Optional[NoteModel]:
        if note_instance.is_password:
            is_password_valid = self._is_password_valid(
                password_db_instance=note_instance.password,
                password_user_input=password
            )
            if is_password_valid:
                return note_instance
        else:
            return note_instance

    def fetch_password_protected_note_by_id(self, note_id: UUID, password_user_input: str) -> Optional[NoteModel]:
        try:
            note_instance = NoteModel.objects.get(id=note_id)
        except ObjectDoesNotExist:
            note_instance = None

        if note_instance:
            note_instance = self.process_note(note_instance, password_user_input)
            return note_instance

        return None

    def fetch_password_protected_note_by_link_slug(self, link_slug: str, password_user_input: str) -> Optional[NoteModel]:
        try:
            note_instance = NoteModel.objects.get(link_slug=link_slug)
        except ObjectDoesNotExist:
            note_instance = None

        if note_instance:
            note_instance = self.process_note(note_instance, password_user_input)
            return note_instance

        return None


class NoteExpirationService:
    @staticmethod
    def delete_expired_notes():
        settings_timezone = timezone(get_current_timezone().key)
        expired_notes_query = NoteModel.objects.filter(
            ~Q(expiration_type=NoteExpirationChoices.NEVER) &
            ~Q(expiration_type=NoteExpirationChoices.BURN_AFTER_READ)
        ).filter(
            expiration_date__lte=datetime.datetime.now().astimezone(settings_timezone)
        )

        logger.info(f"Notes to delete: {expired_notes_query.count()}")
        expired_notes_query.delete()

    @staticmethod
    def calc_expiration_date(expiration_type: NoteExpirationChoices):
        expiration_date = None
        if expiration_type == NoteExpirationChoices.FIVE_MINUTES:
            expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=+1)
        if expiration_type == NoteExpirationChoices.TEN_MINUTES:
            expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=+10)
        if expiration_type == NoteExpirationChoices.ONE_HOUR:
            expiration_date = datetime.datetime.now() + datetime.timedelta(hours=+1)
        if expiration_type == NoteExpirationChoices.ONE_DAY:
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=+1)
        if expiration_type == NoteExpirationChoices.ONE_WEEK:
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=+7)
        if expiration_type == NoteExpirationChoices.TWO_WEEKS:
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=+14)
        if expiration_type == NoteExpirationChoices.ONE_MONTH:
            expiration_date = datetime.datetime.now() + relativedelta(months=+1)
        if expiration_type == NoteExpirationChoices.TWO_WEEKS:
            expiration_date = datetime.datetime.now() + relativedelta(months=+2)
        if expiration_type == NoteExpirationChoices.THREE_MONTHS:
            expiration_date = datetime.datetime.now() + relativedelta(months=+3)
        if expiration_type == NoteExpirationChoices.SIX_MONTHS:
            expiration_date = datetime.datetime.now() + relativedelta(months=+6)
        if expiration_type == NoteExpirationChoices.ONE_YEAR:
            expiration_date = datetime.datetime.now() + relativedelta(years=+1)

        settings_timezone = timezone(get_current_timezone().key)
        return expiration_date.astimezone(settings_timezone)

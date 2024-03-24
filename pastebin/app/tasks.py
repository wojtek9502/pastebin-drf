from celery import shared_task

from .services import NoteExpirationService


@shared_task()
def delete_expired_notes_task():
    NoteExpirationService.delete_expired_notes()

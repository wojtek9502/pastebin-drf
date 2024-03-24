cd pastebin
celery -A app worker --beat --scheduler django -l INFO
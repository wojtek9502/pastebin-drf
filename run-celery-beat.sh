cd pastebin
python -m celery -A app worker --beat --scheduler django -l INFO
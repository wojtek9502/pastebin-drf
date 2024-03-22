import secrets
from hashlib import sha256


def get_note_link_slug():
    link_base = secrets.token_urlsafe(4089)
    link_slug = sha256(link_base.encode('utf-8')).hexdigest()
    return link_slug

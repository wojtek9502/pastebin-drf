import dataclasses
import hashlib
import os
import secrets


@dataclasses.dataclass
class PasswordHashDTO:
    password_hash: bytes
    salt: bytes


class PasswordHashService:
    NOTE_PASSWORDS_SALT_TOKEN_BYTES = int(os.environ['NOTE_PASSWORDS_SALT_TOKEN_BYTES'])
    NOTE_PASSWORDS_HASH_N_ITERATIONS = int(os.environ['NOTE_PASSWORDS_HASH_N_ITERATIONS'])

    def create_hash(self, password_clear: str, iterations: int = None, salt: bytes = None) -> PasswordHashDTO:
        pepper = os.environ['NOTE_PASSWORDS_PEPPER']
        if not iterations:
            iterations = self.NOTE_PASSWORDS_HASH_N_ITERATIONS

        if not salt:
            salt = secrets.token_bytes(self.NOTE_PASSWORDS_SALT_TOKEN_BYTES)

        hash_value = hashlib.pbkdf2_hmac(
            'sha256',
            password_clear.encode('utf-8') + pepper.encode('utf-8'),
            salt,
            iterations
        )
        hash_obj = PasswordHashDTO(salt=salt, password_hash=hash_value)
        return hash_obj


import bcrypt

from ..settings import get_app_settings

settings = get_app_settings()


def generate_app_salt(rounds: int = 15):
    salt = bcrypt.gensalt(rounds = rounds)
    return salt


def get_password_hash(password: str) -> str:
    salt = generate_app_salt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_password_string = hashed_password.decode('utf-8')
    return hashed_password_string
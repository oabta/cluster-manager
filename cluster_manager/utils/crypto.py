import secrets


def generate_password():
    return secrets.token_urlsafe(20)

import uuid


def generate_uuid():
    """Does what it says on the tin."""

    value = uuid.uuid4().hex

    return value

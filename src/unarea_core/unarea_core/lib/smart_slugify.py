from slugify import slugify as awesome_slugify


def slugify(text):
    return awesome_slugify(text).lower()

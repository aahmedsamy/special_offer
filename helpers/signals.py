from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings

from .os import (
    check_file_existance,
    check_directory_existance,
    delete_file,
)

BASE_DIR = settings.BASE_DIR

MODELS_HAS_IMAGE_OR_FILE_FIELD = [
    # accounts
    # contacts
    # properties
    'PropertyImage',
    'PropertyExtra',
]


def valid_model(model):
    return model in MODELS_HAS_IMAGE_OR_FILE_FIELD


def get_image_field_name(model):
    
    for field in ["image", "icon"]:
        if hasattr(model, str(field)):
            image = field
            break
    if hasattr(model, "small_image_path"):
        small = "small_image_path"
    else:
        small = None
    return (field, small)


@receiver([post_delete])
def post_delete_image_delete(sender, instance, **kwargs):
    if not valid_model(sender.__name__):
        return
    image, small = get_image_field_name(sender)
    paths = []
    paths.append(getattr(instance, image).path)
    if small:
        paths.append(BASE_DIR+getattr(instance, small))
    delete_file(paths)
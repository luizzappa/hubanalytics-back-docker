import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Images

@receiver(post_delete, sender=Images)
def delete_files(sender, instance, *args, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
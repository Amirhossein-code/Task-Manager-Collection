from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from ..models import Individual


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_individual_profile_for_new_user(sender, **kwargs):
    """
    As the name suggests when a new user is created a profile for that user is
    created by utilizing the Individual Model
    """
    if kwargs["created"]:
        Individual.objects.create(user=kwargs["instance"])

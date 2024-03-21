from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from app.models import Individual


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_individual_profile_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Individual.objects.create(user=kwargs["instance"])

from sendmail.tasks import send_change_access_recipe
from .models import Recipes
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Recipes)
def change_access_recipe(sender, instance, *args, **kwargs):
    if instance.access == 'public':
        send_change_access_recipe.delay(instance.id)

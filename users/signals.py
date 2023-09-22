from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def update_total_users(sender, instance=None, created=False, **kwargs):
    if created:
        User = get_user_model()
        User.objects.update(total_users=User.objects.count())

from allauth.account.models import EmailAddress
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_user_information(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        updated_email = instance.email
        try:
            current_email = EmailAddress.objects.get_primary(instance)
            if current_email.email != updated_email:
                current_email.email = updated_email
                current_email.verified = False
                current_email.save()
        except:
            EmailAddress.objects.create(
                user=instance,
                email=updated_email,
                primary=True,
                verified=False,
            )


@receiver(pre_save, sender=User)
def standardize_signup_user_information(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

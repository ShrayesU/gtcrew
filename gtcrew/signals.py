from allauth.account.signals import user_signed_up
from django.conf import settings
from django.contrib.auth.models import Group
from django.dispatch import receiver


@receiver(user_signed_up)
def add_user_to_public_group(sender, **kwargs):
    user = kwargs.get('user', None)
    user.groups.add(Group.objects.get(pk=settings.PUBLIC_GROUP_ID))

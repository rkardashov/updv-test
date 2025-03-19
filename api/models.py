import binascii
import os
from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from .helpers import get_idtype, IDTypes


class ExpirableToken(models.Model):
    key = models.CharField("Key", max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name="User"
    )
    created = models.DateTimeField("Created", auto_now_add=True)
    expires_at = models.DateTimeField("Expires at", default=timezone.now)

    class Meta:
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "ExpirableToken"
        verbose_name_plural = "ExpirableTokens"
        ordering = ["-expires_at"]

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        self.expires_at = timezone.now() + timedelta(minutes=settings.TOKEN_LIFETIME_MINUTES)
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_type = models.CharField(max_length=16, choices=IDTypes.choices, default=IDTypes.UNKNOWN)

    def save(self, **kwargs):
        self.id_type = get_idtype(self.user.username)
        return super().save(**kwargs)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_related_objects(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    ExpirableToken.objects.create(user=instance)

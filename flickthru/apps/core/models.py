from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_superuser, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_superuser=is_superuser,
            is_staff=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model for users
    """
    username = models.CharField(
        unique=False,
        max_length=150,
        blank=False,
    )
    email = models.CharField(
        unique=True,
        max_length=150,
        blank=False,
    )
    is_staff = models.BooleanField(default=False)
    # Additional fields
    param1 = models.TextField(null=True, blank=True)
    param2 = models.TextField(null=True, blank=True)
    param3 = models.TextField(null=True, blank=True)
    param4 = models.TextField(null=True, blank=True)
    param5 = models.TextField(null=True, blank=True)
    param6 = models.TextField(null=True, blank=True)
    param7 = models.TextField(null=True, blank=True)
    param8 = models.TextField(null=True, blank=True)
    param9 = models.TextField(null=True, blank=True)
    param10 = models.TextField(null=True, blank=True)

    facebook_first_name = models.TextField(null=True, blank=True)
    facebook_last_name = models.TextField(null=True, blank=True)
    facebook_verified = models.TextField(null=True, blank=True)
    facebook_name = models.TextField(null=True, blank=True)
    facebook_locale = models.TextField(null=True, blank=True)
    facebook_gender = models.TextField(null=True, blank=True)
    facebook_age_range = models.TextField(null=True, blank=True)
    facebook_updated_time = models.TextField(null=True, blank=True)
    facebook_link = models.TextField(null=True, blank=True)
    facebook_id = models.TextField(null=True, blank=True)
    facebook_timezone = models.TextField(null=True, blank=True)
    facebook_picture = models.TextField(null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def get_short_name(self):
        return unicode(self)

    class Meta:
        app_label = 'core'


class TitledImage(models.Model):
    """
    Model for images
    """
    id = models.PositiveIntegerField(primary_key=True)
    subscription_id = models.IntegerField()
    object_id = models.CharField(max_length=180, blank=True, null=True)
    subscription_object = models.CharField(max_length=180, blank=True,
                                           null=True)
    media_username = models.CharField(max_length=180, blank=True, null=True)
    media_profile_picture = models.CharField(max_length=180, blank=True,
                                             null=True)
    media_user_id = models.CharField(max_length=180, blank=True, null=True)
    media_standard_resolution_url = models.CharField(max_length=180,
                                                     blank=True, null=True)
    media_like_count = models.IntegerField(blank=True, null=True)
    media_id = models.CharField(max_length=180, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('id', 'subscription_id'),)

    def __unicode__(self):
        return "%s Image" % self.id


class Like(models.Model):
    """
    Model for image likes
    """
    image = models.ForeignKey(TitledImage, related_name='estimated_images')
    user = models.ForeignKey(User, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s Like " % self.id

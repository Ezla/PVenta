from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User


def url(obj, filename):
    ruta = 'usuarios/%s/foto-%s.%s' % (obj.user.username, obj.user.username, filename.split('.')[-1])
    return ruta


class UserProfile(models.Model):
    avatar = models.ImageField(upload_to=url)
    user = models.OneToOneField(User, related_name="profile")
    STATUS_TEMPLATE = ((1, 'Predeterminado'), (2, 'Clasico'),)
    plantilla = models.IntegerField(choices=STATUS_TEMPLATE, default=1)

    def __unicode__(self):
        return self.user.username

    def get_avatar(self):
        return '<img src="%s" width="70" height="70"/>' % self.avatar.url

    get_avatar.short_description = 'Thumb'
    get_avatar.allow_tags = True


# class UserManager(BaseUserManager, models.Manager):
#
#     def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
#         email = self.normalize_email(email)
#         if not email:
#             raise ValueError('El email es un campo obligatorio.')
#         user = self.model(username=username, email=email, is_staff=is_staff, is_superuser=is_superuser)
#         user.set_password(password)
#         user.save(using=self._db)
#
#     def create_user(self, username, email, password=None, **extra_fields):
#         return self._create_user(username, email, password, False, False, **extra_fields)
#
#     def create_superuser(self, username, email, password=None, **extra_fields):
#         return self._create_user(username, email, password, True, True, **extra_fields)
#
#
# class User(AbstractBaseUser,PermissionsMixin):
#     username = models.CharField(unique=True, max_length=50)
#     email = models.EmailField()
#     first_name = models.CharField(max_length=70)
#     last_name = models.CharField(max_length=100)
#     address = models.CharField(max_length=150)
#     avatar = models.ImageField(upload_to=url)
#
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     object = UserManager()
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     def get_short_name(self):
#         return '%s %s' % (self.first_name, self.last_name)
# imports
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# rest framework imports
from rest_framework.authtoken.models import Token


# Create your models here.


class MyAccountManager(BaseUserManager):  # creating custom user manager
    def create_user(self, ph_num, email, username, password=None):  # creating manager
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            ph_num=ph_num,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # creating manager superuser
    def create_superuser(self, ph_num, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            ph_num=ph_num,
            password=password,
            username=username,
        )

        # giving managing abilities
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):  # creating custom/abstract user

    REQUIRED_FIELDS = ('ph_num', 'email')
    USERNAME_FIELD = 'username'

    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    ph_num = models.CharField(
        max_length=10, unique=False, verbose_name='phone number')
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

# creating reciever for automatic creation of auth tokens
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

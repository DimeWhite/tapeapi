from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class EmailUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        user = User.objects.create(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ("FOLLOWER", 'Follower'),
        ("AUTHOR", 'Author')
    )
    username = None
    email = models.EmailField(unique=True, null=False, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists."
                                }
                              )
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, null=False, default=0)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = EmailUserManager()

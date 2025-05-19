from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # class Meta:
    #     unique_together = ('user', 'email')
    pass
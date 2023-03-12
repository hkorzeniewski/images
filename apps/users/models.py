from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.tiers.models import AccountTier

# Create your models here.


class User(AbstractUser):
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)

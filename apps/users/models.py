from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.tiers.models import AccountTier

# Create your models here.

class User(AbstractUser):
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE, default=AccountTier.get_default_pk)

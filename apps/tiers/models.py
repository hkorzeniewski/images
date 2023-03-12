from django.db import models

# Create your models here.


class AccountTier(models.Model):
    tier_name = models.CharField(max_length=256)
    thumbnail_size = models.IntegerField(null=True)
    presence_of_original_link = models.BooleanField(default=False)
    ability_to_expiring_links = models.BooleanField(default=False)

    @classmethod
    def get_default_pk(cls):
        tier, created = cls.objects.get_or_create(tier_name="BASIC")
        return tier.pk

    def __str__(self) -> str:
        return self.tier_name

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.tiers.models import AccountTier

class BuiltInTiers(BaseCommand):
    help = "Add built in tiers"

    def handle(self, *args, **kwargs):
        AccountTier.objects.create(tier_name='BASIC', thumbnail_size=200)
        AccountTier.objects.create(tier_name='PREMIUM', thumbnail_size=400, presence_of_original_link=True)
        AccountTier.objects.create(tier_name='ENTERPRISE', thumbnail_size=400, presence_of_original_link=True, ability_to_expiring_links=True)
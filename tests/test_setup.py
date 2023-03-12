import os
import tempfile
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            SimpleUploadedFile)
from django.shortcuts import render
from django.test import TestCase
from django.urls import ResolverMatch, resolve
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.tiers.models import AccountTier
from apps.users.models import User

# Create your tests here.


class BaseTestCase(APITestCase):
    def setUp(self):
        self.basic_username = "basicuser"
        self.premium_username = "premiumuser"
        self.enterprise_username = "enterpriseuser"

        self.email = "test@user.com"
        self.password = "testuser1234"
        self.basic_account_tier = AccountTier.objects.create(
            tier_name="BASIC", thumbnail_size=200
        )
        self.premium_account_tier = AccountTier.objects.create(
            tier_name="PREMIUM", thumbnail_size=400, presence_of_original_link=True
        )
        self.enterprise_account_tier = AccountTier.objects.create(
            tier_name="ENTERPRISE",
            thumbnail_size=400,
            presence_of_original_link=True,
            ability_to_expiring_links=True,
        )

        self.basic_user = User.objects.create_user(
            username=self.basic_username, account_tier=self.basic_account_tier
        )
        self.premium_user = User.objects.create_user(
            username=self.premium_username, account_tier=self.premium_account_tier
        )
        self.enterprise_user = User.objects.create_user(
            username=self.enterprise_username, account_tier=self.enterprise_account_tier
        )

from django.db import models
from purchase.models.choices import Platform


class Subscription(models.Model):
    user = models.UUIDField()
    subscription_id = models.CharField(max_length=2048)
    platform = models.CharField(max_length=8, choices=Platform.choices)
    active_till = models.DateTimeField()
    google_token = models.CharField(null=True, max_length=8192, help_text="Only for android platform")

from django.db import models


class Platform(models.TextChoices):
    ios = "ios", "Ios"
    android = "android", "Android"


class PurchaseResponseStatus(models.TextChoices):
    ok = "ok"
    purchase_already_created = "purchase already created"
    data_is_not_valid = "data is not valid"
    error = "error"

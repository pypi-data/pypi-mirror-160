from django.urls import path

from .views import ProcessPurchaseView, LogConfig

urlpatterns = [
    path("chargeverify/", ProcessPurchaseView.as_view(), name="ChargeVerify"),
    path("logconfig/", LogConfig.as_view(), name="LogConfig"),
]

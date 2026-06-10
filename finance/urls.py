from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("pago/nuevo/", views.payment_create, name="payment_create"),
    path("pago/<int:pk>/toggle/", views.payment_toggle, name="payment_toggle"),
]

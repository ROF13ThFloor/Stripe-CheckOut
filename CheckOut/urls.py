from django.urls import path
from . import views


urlpatterns = [
    path('', views.CheckOutPage.as_view(), name='CheckoutPage'),
]
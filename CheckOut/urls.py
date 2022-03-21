from django.urls import path
from . import views


urlpatterns = [
    path('', views.CheckOutPage.as_view(), name='CheckOut'),
    path('config/' , views.pub_keyrequets),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.SuccessPage.as_view()),
    path('webhook/', views.check_webhook),


]
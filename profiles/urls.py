from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('NewsLetter', views.add_NewsLetter, name='NewsLetter'),
    path('ContactUsForm', views.add_ContactUs, name='ContactUsForm'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]
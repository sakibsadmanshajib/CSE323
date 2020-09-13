"""
Definition of urls for CSE323.app.
"""

from django.urls import path
from app import forms, views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]

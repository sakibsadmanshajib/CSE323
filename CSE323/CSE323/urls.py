"""
Definition of urls for CSE323.
"""

from datetime import datetime
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

urlpatterns = [
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('jobs/', views.getCurrentJobs, name='getCurrentJobs'),
    path('jobs/add/', views.addJob, name='addJob'),
    path('jobs/update/', views.updateJobs, name='updateJobs'),
    path('pastjobs/', views.getPastJobs, name='getPastJobs'),
]

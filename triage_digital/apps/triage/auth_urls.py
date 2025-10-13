"""
URLs de autenticación personalizada con DNI
"""
from django.urls import path
from . import auth_views

urlpatterns = [
    path('', auth_views.login_profesional, name='login'),
    path('logout/', auth_views.logout_profesional, name='logout'),
]
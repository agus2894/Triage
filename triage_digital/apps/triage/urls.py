"""
URLs del sistema de triage - Solo rutas esenciales.
Filosofía: "Menos es mejor"
"""

from django.urls import path
from . import views

app_name = 'triage'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_principal, name='dashboard'),
    
    # Gestión de pacientes
    path('paciente/nuevo/', views.registrar_paciente, name='registrar_paciente'),
    path('paciente/lista/', views.lista_pacientes, name='lista_pacientes'),
    path('paciente/<int:paciente_id>/atendido/', views.marcar_atendido, name='marcar_atendido'),
    
    # Signos vitales y triage
    path('signos/<int:paciente_id>/', views.cargar_signos_vitales, name='cargar_signos'),
    
    # API simple
    path('api/paciente/<int:paciente_id>/', views.api_estado_paciente, name='api_paciente'),
]
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
    
    # NUEVO: Triage completo en una sola página
    path('triage-completo/', views.triage_completo, name='triage_completo'),
    
    # Gestión de pacientes - Solo lo esencial
    path('paciente/<int:paciente_id>/atendido/', views.marcar_atendido, name='marcar_atendido'),
    
    # Signos vitales y triage
    path('signos/<int:paciente_id>/', views.cargar_signos_vitales, name='cargar_signos'),
    
    # API simple
    path('api/lista-pacientes/', views.api_lista_pacientes, name='api_lista_pacientes'),
]
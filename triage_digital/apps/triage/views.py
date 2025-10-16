"""
Vistas principales del sistema de triage médico.
Filosofía: "Menos es mejor" - Funciones simples que salvan vidas.
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger('apps.triage')

from apps.patients.models import Paciente
from .models import SignosVitales, TriageResult, Profesional



@login_required
@require_http_methods(["GET", "POST"])
def triage_completo(request):
    """
    Formulario unificado: Registro de paciente + Signos vitales + Triage en una sola pantalla.
    GAME CHANGER: Todo el flujo médico en una sola vista.
    """
    if request.method == 'POST':
        try:
            # Obtener el profesional asociado al usuario
            try:
                profesional = request.user.profesional
            except Profesional.DoesNotExist:
                messages.error(request, 'Usuario no tiene perfil de profesional asociado.')
                return redirect('triage:dashboard')
            
            # 1. Crear paciente con datos opcionales
            nombre = request.POST.get('nombre', '').strip() or None
            apellido = request.POST.get('apellido', '').strip() or None
            dni = request.POST.get('dni', '').strip() or None
            edad = request.POST.get('edad')
            
            paciente = Paciente.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                edad=int(edad) if edad else None,
                motivo_consulta=request.POST.get('motivo_consulta', '').strip()
            )
            
            # 2. Crear signos vitales (auto-calcula triage en save())
            signos = SignosVitales.objects.create(
                paciente=paciente,
                profesional=profesional,
                frecuencia_respiratoria=int(request.POST['frecuencia_respiratoria']),
                saturacion_oxigeno=int(request.POST['saturacion_oxigeno']),
                tension_sistolica=int(request.POST['tension_sistolica']),
                frecuencia_cardiaca=int(request.POST['frecuencia_cardiaca']),
                nivel_conciencia=request.POST['nivel_conciencia'],
                temperatura=float(request.POST['temperatura'])
            )
            
            # 3. Obtener resultado del triage
            resultado = TriageResult.objects.get(signos_vitales=signos)
            
            # 4. Mensaje de éxito con toda la información
            messages.success(
                request, 
                f'Triage completado para {paciente.nombre_completo}: '
                f'{resultado.nivel_urgencia} (NEWS: {resultado.news_score}) - '
                f'Tiempo máximo: {resultado.tiempo_atencion_max} minutos'
            )
            
            return redirect('triage:dashboard')
            
        except Exception as e:
            messages.error(request, f'Error al completar triage: {str(e)}')
    
    return render(request, 'triage/triage_completo.html')


@login_required
@require_http_methods(["GET", "POST"])
def cargar_signos_vitales(request, paciente_id):
    """
    Carga de signos vitales y cálculo automático de triage.
    CRÍTICO: Esta función puede salvar vidas.
    """
    paciente = get_object_or_404(Paciente, id=paciente_id, activo=True)
    
    if request.method == 'POST':
        try:
            # Obtener el profesional asociado al usuario
            try:
                profesional = request.user.profesional
            except Profesional.DoesNotExist:
                messages.error(request, 'Usuario no tiene perfil de profesional asociado.')
                return redirect('triage:dashboard')
            
            # Crear signos vitales (auto-calcula triage en save())
            signos = SignosVitales.objects.create(
                paciente=paciente,
                profesional=profesional,
                frecuencia_respiratoria=int(request.POST['frecuencia_respiratoria']),
                saturacion_oxigeno=int(request.POST['saturacion_oxigeno']),
                tension_sistolica=int(request.POST['tension_sistolica']),
                frecuencia_cardiaca=int(request.POST['frecuencia_cardiaca']),
                nivel_conciencia=request.POST['nivel_conciencia'],
                temperatura=float(request.POST['temperatura'])
            )
            
            # Solo log en caso de error crítico (removido logging innecesario)
            
            # Obtener resultado del triage
            resultado = TriageResult.objects.get(signos_vitales=signos)
            
            messages.success(
                request, 
                f'Triage calculado: {resultado.nivel_urgencia} - '
                f'Tiempo máximo: {resultado.tiempo_atencion_max} minutos'
            )
            
            return redirect('triage:dashboard')
            
        except Exception as e:
            messages.error(request, f'Error al procesar signos vitales: {str(e)}')
    
    context = {
        'paciente': paciente,
        'conciencia_choices': SignosVitales.CONCIENCIA_CHOICES
    }
    return render(request, 'triage/cargar_signos.html', context)


@login_required
def dashboard_principal(request):
    """
    Dashboard médico optimizado - Vista general del triage.
    Caché de 2 minutos para estadísticas no críticas.
    """
    # Estadísticas en tiempo real (últimas 24 horas)
    hace_24h = timezone.now() - timedelta(hours=24)
    
    # Intentar obtener estadísticas del caché
    cache_key = f'dashboard_stats_{hace_24h.strftime("%Y%m%d_%H")}'
    estadisticas = cache.get(cache_key)
    
    if estadisticas is None:
        # Contadores por urgencia
        estadisticas = TriageResult.objects.filter(
            fecha_calculo__gte=hace_24h
        ).aggregate(
            total=Count('id'),
            rojos=Count('id', filter=Q(nivel_urgencia='ROJO')),
            amarillos=Count('id', filter=Q(nivel_urgencia='AMARILLO')),
            verdes=Count('id', filter=Q(nivel_urgencia='VERDE'))
        )
        # Guardar en caché por 2 minutos
        cache.set(cache_key, estadisticas, 120)
    
    # Cache casos críticos por 1 minuto (datos más críticos)
    criticos_key = f'casos_criticos_{hace_24h.strftime("%Y%m%d_%H%M")}'
    casos_criticos = cache.get(criticos_key)
    if casos_criticos is None:
        casos_criticos = list(TriageResult.objects.filter(
            nivel_urgencia__in=['ROJO', 'AMARILLO'],
            signos_vitales__paciente__activo=True
        ).select_related(
            'signos_vitales__paciente',
            'signos_vitales__profesional__user'
        ).order_by('-fecha_calculo')[:10])
        cache.set(criticos_key, casos_criticos, 60)
    
    # Cache pacientes pendientes (no atendidos) por 2 minutos
    pacientes_key = 'pacientes_pendientes'
    pacientes_recientes = cache.get(pacientes_key)
    if pacientes_recientes is None:
        pacientes_recientes = list(Paciente.objects.filter(
            activo=True,
            estado_atencion__in=['ESPERANDO', 'EN_ATENCION']
        ).order_by('-fecha_ingreso')[:5])
        cache.set(pacientes_key, pacientes_recientes, 120)
    
    context = {
        'estadisticas': estadisticas,
        'casos_criticos': casos_criticos,
        'pacientes_recientes': pacientes_recientes,
    }
    
    return render(request, 'triage/dashboard.html', context)




@login_required
@require_http_methods(["POST"])
def marcar_atendido(request, paciente_id):
    """Marca un paciente como atendido (AJAX)."""
    try:
        paciente = get_object_or_404(Paciente, id=paciente_id, activo=True)
        paciente.marcar_atendido()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Paciente {paciente.nombre_completo} marcado como atendido',
            'estado': paciente.get_estado_atencion_display(),
            'tiempo': paciente.tiempo_espera
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def api_lista_pacientes(request):
    """
    API para obtener lista de pacientes en espera (sidebar en tiempo real).
    """
    try:
        # Obtener pacientes en espera - simple y sin errores
        pacientes = Paciente.objects.filter(
            activo=True,
            estado_atencion='ESPERANDO'
        ).order_by('-fecha_ingreso')
        
        data = []
        for paciente in pacientes:
            try:
                # Obtener último triage si existe
                nivel_urgencia = 'SIN TRIAGE'
                ultimo_signo = paciente.signos_vitales.first()
                if ultimo_signo:
                    try:
                        resultado = TriageResult.objects.get(signos_vitales=ultimo_signo)
                        nivel_urgencia = resultado.nivel_urgencia
                    except TriageResult.DoesNotExist:
                        pass
                
                data.append({
                    'id': paciente.id,
                    'nombre_completo': paciente.nombre_completo,
                    'dni': paciente.dni or 'Sin DNI',
                    'edad': paciente.edad,
                    'tiempo_espera': paciente.tiempo_espera,
                    'tiempo_espera_minutos': paciente.tiempo_espera_minutos,
                    'nivel_urgencia': nivel_urgencia,
                    'motivo_consulta': paciente.motivo_consulta or ''
                })
            except Exception as e:
                logger.error(f"Error procesando paciente {paciente.id}: {str(e)}")
                continue  # Saltar este paciente pero seguir con los demás
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        logger.error(f"Error en API lista pacientes: {str(e)}")
        return JsonResponse({'error': 'Error interno del servidor', 'detail': str(e)}, status=500)

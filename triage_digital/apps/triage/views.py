"""
Vistas principales del sistema de triage médico.
Filosofía: "Menos es mejor" - Funciones simples que salvan vidas.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

# PDF ultra-simple
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from apps.patients.models import Paciente
from .models import SignosVitales, Profesional


def _crear_signos_vitales(request, paciente, profesional):
    """
    Helper function para crear signos vitales y calcular triage.
    Aplicando DRY principle - "Menos es más".
    """
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
    
    return signos


def _obtener_profesional(request):
    """Helper para obtener profesional del usuario actual."""
    try:
        return request.user.profesional
    except Profesional.DoesNotExist:
        return None



@login_required
@require_http_methods(["GET", "POST"])
def triage_completo(request):
    """
    Vista única inteligente para triage médico.
    MENOS ES MÁS: Maneja tanto pacientes conscientes como inconscientes en una sola pantalla.
    """
    if request.method == 'POST':
        try:
            # Obtener profesional
            profesional = _obtener_profesional(request)
            if not profesional:
                messages.error(request, 'Usuario no tiene perfil de profesional asociado.')
                return redirect('triage:dashboard')
            
            # Detectar si es paciente inconsciente
            es_inconsciente = request.POST.get('es_inconsciente') == 'on'
            
            # 1. Crear paciente con datos adaptativos
            if es_inconsciente:
                # Paciente crítico: solo datos esenciales
                paciente = Paciente.objects.create(
                    nombre='PACIENTE',
                    apellido='CRÍTICO',
                    dni=None,
                    edad=None,
                    motivo_consulta='EMERGENCIA - PACIENTE INCONSCIENTE'
                )
            else:
                # Paciente consciente: datos completos
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
            
            # 2. Crear signos vitales usando helper
            signos = _crear_signos_vitales(request, paciente, profesional)
            
            # 3. Mensaje de éxito adaptativo
            if es_inconsciente:
                messages.warning(
                    request, 
                    f'🚨 PACIENTE CRÍTICO registrado: {signos.nivel_urgencia} (NEWS: {signos.news_score}) - '
                    f'ATENCIÓN INMEDIATA requerida'
                )
            else:
                messages.success(
                    request, 
                    f'Triage completado para {paciente.nombre_completo}: '
                    f'{signos.nivel_urgencia} (NEWS: {signos.news_score}) - '
                    f'Tiempo máximo: {signos.tiempo_atencion_max} minutos'
                )
            
            return redirect('triage:dashboard')
            
        except Exception as e:
            messages.error(request, f'Error al completar triage: {str(e)}')
    
    return render(request, 'triage/triage_completo.html')


@login_required
def dashboard_principal(request):
    """
    Dashboard médico optimizado - Vista general del triage.
    🚨 TIEMPO REAL para casos críticos - Sin cache para emergencias.
    """
    # Estadísticas en tiempo real (últimas 24 horas)
    hace_24h = timezone.now() - timedelta(hours=24)
    
    # 🔥 SIN CACHE - Datos críticos en tiempo real
    # Contadores por urgencia usando signos vitales - SOLO PACIENTES SIN ATENDER
    estadisticas = SignosVitales.objects.filter(
        fecha_hora__gte=hace_24h,
        nivel_urgencia__isnull=False,
        paciente__activo=True,
        paciente__estado_atencion__in=['ESPERANDO', 'EN_ATENCION']  # 🎯 SOLO SIN ATENDER
    ).aggregate(
        total=Count('id'),
        rojos=Count('id', filter=Q(nivel_urgencia='ROJO')),
        amarillos=Count('id', filter=Q(nivel_urgencia='AMARILLO')),
        verdes=Count('id', filter=Q(nivel_urgencia='VERDE'))
    )
    
    # Casos críticos - SOLO pacientes sin atender (TIEMPO REAL)
    casos_criticos = list(SignosVitales.objects.filter(
        nivel_urgencia__in=['ROJO', 'AMARILLO'],
        paciente__activo=True,
        paciente__estado_atencion__in=['ESPERANDO', 'EN_ATENCION']  # 🎯 FILTRO CLAVE
    ).select_related(
        'paciente',
        'profesional__user'
    ).order_by('-fecha_hora')[:10])
    
    # Pacientes pendientes (TIEMPO REAL)
    pacientes_recientes = list(Paciente.objects.filter(
        activo=True,
        estado_atencion__in=['ESPERANDO', 'EN_ATENCION']
    ).order_by('-fecha_ingreso')[:5])
    
    stats = {
        'estadisticas': estadisticas,
        'casos_criticos': casos_criticos,
        'pacientes_recientes': pacientes_recientes,
    }
    
    return render(request, 'triage/dashboard.html', stats)




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
                if ultimo_signo and ultimo_signo.nivel_urgencia:
                    nivel_urgencia = ultimo_signo.nivel_urgencia
                
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
            except Exception:
                continue  # Saltar este paciente pero seguir con los demás
        
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)


@login_required
def reporte_diario_pdf(request):
    """
    🎯 REPORTE PDF ULTRA-SIMPLE: Una página, datos esenciales.
    Filosofía "Menos es Más": Solo lo que importa para salvar vidas.
    """
    # Datos del día actual
    hoy = timezone.now().date()
    
    # Estadísticas en 4 líneas
    total = SignosVitales.objects.filter(fecha_hora__date=hoy).count()
    rojos = SignosVitales.objects.filter(fecha_hora__date=hoy, nivel_urgencia='ROJO').count()
    amarillos = SignosVitales.objects.filter(fecha_hora__date=hoy, nivel_urgencia='AMARILLO').count()
    verdes = SignosVitales.objects.filter(fecha_hora__date=hoy, nivel_urgencia='VERDE').count()
    
    # Crear PDF ultra-minimalista
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="triage_diario_{hoy}.pdf"'
    
    # PDF de 1 página
    p = canvas.Canvas(response, pagesize=letter)
    
    # Header médico
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, 750, f"🏥 REPORTE TRIAGE DIARIO - {hoy.strftime('%d/%m/%Y')}")
    
    # Datos esenciales
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 700, "📊 RESUMEN DEL DÍA:")
    
    p.setFont("Helvetica", 14)
    p.drawString(70, 670, f"🔴 CRÍTICOS (ROJO): {rojos} pacientes")
    p.drawString(70, 650, f"🟡 MODERADOS (AMARILLO): {amarillos} pacientes")
    p.drawString(70, 630, f"🟢 ESTABLES (VERDE): {verdes} pacientes")
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(70, 600, f"📈 TOTAL ATENDIDOS: {total} pacientes")
    
    # Pie simple
    p.setFont("Helvetica", 10)
    p.drawString(50, 50, f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M')} | Sistema Triage Digital")
    
    p.showPage()
    p.save()
    
    return response


def manifest(request):
    """
    📱 PWA Manifest - Configuración para app instalable.
    Permite instalar Triage Digital como app nativa.
    """
    return render(request, 'triage/manifest.json', content_type='application/manifest+json')


def service_worker(request):
    """
    🔧 Service Worker - Funcionalidad offline para emergencias.
    Permite usar el sistema sin conexión en situaciones críticas.
    """
    return render(request, 'triage/sw.js', content_type='application/javascript')

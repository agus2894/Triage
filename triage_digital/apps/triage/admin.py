from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import SignosVitales, Profesional


class ProfesionalForm(forms.ModelForm):
    """Formulario personalizado para crear profesionales directamente."""
    
    nombre = forms.CharField(max_length=30, label="Nombre")
    apellido = forms.CharField(max_length=30, label="Apellido") 
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    
    class Meta:
        model = Profesional
        fields = ['dni', 'tipo', 'matricula', 'activo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.user:
            self.fields['nombre'].initial = self.instance.user.first_name
            self.fields['apellido'].initial = self.instance.user.last_name
            self.fields['password'].required = False
            self.fields['password'].help_text = "Dejar en blanco para mantener la actual"


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    """Admin simplificado - Crear profesionales fácilmente."""
    form = ProfesionalForm
    list_display = ('get_nombre_completo', 'dni', 'tipo', 'matricula', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('dni', 'user__first_name', 'user__last_name')
    
    fieldsets = (
        ('Datos del Profesional', {
            'fields': ('nombre', 'apellido', 'password')
        }),
        ('Información Médica', {
            'fields': ('dni', 'tipo', 'matricula', 'activo')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Crear User automáticamente al crear Profesional."""
        if not change:  # Solo al crear
            user = User.objects.create_user(
                username=obj.dni,
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['nombre'],
                last_name=form.cleaned_data['apellido'],
                email=f"{obj.dni}@hospital.com"
            )
            obj.user = user
        else:  # Al editar
            if obj.user:
                obj.user.first_name = form.cleaned_data['nombre']
                obj.user.last_name = form.cleaned_data['apellido']
                if form.cleaned_data['password']:
                    obj.user.set_password(form.cleaned_data['password'])
                obj.user.save()
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        """Eliminar también el usuario asociado."""
        user = obj.user
        super().delete_model(request, obj)
        if user and user.username != 'admin':
            user.delete()
    
    def delete_queryset(self, request, queryset):
        """Eliminar usuarios en eliminación masiva."""
        users_to_delete = []
        for obj in queryset:
            if obj.user and obj.user.username != 'admin':
                users_to_delete.append(obj.user)
        
        super().delete_queryset(request, queryset)
        
        for user in users_to_delete:
            user.delete()
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name() if obj.user else f"Prof {obj.dni}"
    get_nombre_completo.short_description = 'Nombre Completo'


# Ocultar User del admin - Solo gestionar Profesionales
admin.site.unregister(User)

# Personalizar títulos del admin
admin.site.site_header = "🏥 Triage Digital - Administración"
admin.site.site_title = "Triage Admin"
admin.site.index_title = "Gestión de Profesionales Médicos"


@admin.register(SignosVitales)
class SignosVitalesAdmin(admin.ModelAdmin):
    """
    Configuración del admin para SignosVitales (incluye resultado de triage).
    """
    list_display = ('paciente', 'profesional', 'fecha_hora', 'news_score', 
                   'nivel_urgencia', 'tiempo_atencion_max')
    list_filter = ('nivel_urgencia', 'fecha_hora', 'news_score')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'paciente__dni')
    readonly_fields = ('fecha_hora', 'news_score', 'nivel_urgencia', 
                      'tiempo_atencion_max', 'color_hex')
    list_per_page = 20
    
    fieldsets = (
        ('Paciente y Profesional', {
            'fields': ('paciente', 'profesional', 'fecha_hora')
        }),
        ('Signos Vitales', {
            'fields': ('frecuencia_respiratoria', 'saturacion_oxigeno', 
                      'tension_sistolica', 'frecuencia_cardiaca', 
                      'nivel_conciencia', 'temperatura')
        }),
        ('Resultado Triage (Automático)', {
            'fields': ('news_score', 'nivel_urgencia', 'tiempo_atencion_max', 'color_hex')
        }),
    )

from django.contrib import admin
from .models import Certificado, Evento


class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('certificado', 'participante', 'evento')

class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criador', 'carga_horaria', 'status')

admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(Evento, EventoAdmin)

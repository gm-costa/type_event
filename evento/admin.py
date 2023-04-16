from django.contrib import admin
from .models import Evento


class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criador', 'carga_horaria', 'status')

admin.site.register(Evento, EventoAdmin)

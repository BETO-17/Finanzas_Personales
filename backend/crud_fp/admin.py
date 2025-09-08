"""Configuración del panel de administración para Transaccion."""
from django.contrib import admin
from .models import Transaccion


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    """Personaliza la vista de Transaccion en el admin de Django."""
    list_display = ("idTransaccion", "categoria", "fecha", "monto", "tipo_transac", "estado_transac")
    list_filter = ("tipo_transac", "estado_transac", "fecha", "categoria")
    search_fields = ("idTransaccion", "categoria", "destinatario", "descripcion")


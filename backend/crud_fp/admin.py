from django.contrib import admin
from .models import Transaccion

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'categoria', 'monto', 'fecha', 'descripcion']
    list_filter = ['tipo', 'categoria', 'fecha', 'usuario']
    search_fields = ['descripcion', 'usuario__username']
    list_per_page = 20
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'tipo', 'categoria', 'monto')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'fecha')
        }),
    )

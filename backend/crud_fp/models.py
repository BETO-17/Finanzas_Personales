from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    
    CATEGORIA_CHOICES = [
        ('alimentacion', 'Alimentación'),
        ('transporte', 'Transporte'),
        ('entretenimiento', 'Entretenimiento'),
        ('salud', 'Salud'),
        ('educacion', 'Educación'),
        ('vivienda', 'Vivienda'),
        ('otros', 'Otros'),
        ('salario', 'Salario'),
        ('bonificacion', 'Bonificación'),
        ('inversion', 'Inversión'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacciones')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(default=timezone.now)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.categoria} - ${self.monto}"

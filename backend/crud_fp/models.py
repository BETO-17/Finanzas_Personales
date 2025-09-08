"""Modelos de la aplicación crud_fp.

Contiene la definición del modelo Transaccion, que representa un
movimiento financiero con sus atributos principales (categoría, fecha,
monto, destinatario, tipo, estado y descripción).
"""

from django.db import models


class Transaccion(models.Model):
    """Modelo para almacenar transacciones financieras.

    - tipo_transac: define si es Ingreso, Gasto o Transferencia.
    - estado_transac: indica el estado del movimiento.
    """
    TIPO_TRANSACCION_CHOICES = (
        ("Ingreso", "Ingreso"),
        ("Gasto", "Gasto"),
        ("Transferencia", "Transferencia"),
    )

    ESTADO_TRANSACCION_CHOICES = (
        ("Pendiente", "Pendiente"),
        ("Completada", "Completada"),
        ("Cancelada", "Cancelada"),
    )

    # Identificador propio solicitado por el requerimiento
    idTransaccion = models.AutoField(primary_key=True)
    # Categoría de la transacción, por ejemplo: "Alimentación"
    categoria = models.CharField(max_length=45)
    # Fecha del movimiento
    fecha = models.DateField()
    # Importe del movimiento
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    # Persona o entidad involucrada
    destinatario = models.CharField(max_length=100, default="Desconocido")
    # Tipo de transacción: Ingreso, Gasto o Transferencia
    tipo_transac = models.CharField(max_length=15, choices=TIPO_TRANSACCION_CHOICES)
    # Estado de la transacción: Pendiente, Completada o Cancelada
    estado_transac = models.CharField(
       max_length=20,
       choices=ESTADO_TRANSACCION_CHOICES,
       default='pendiente'   # Valor inicial para registros existentes)
       )
    # Detalle adicional opcional
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "transaccion"
        ordering = ["-fecha", "-idTransaccion"]

    def __str__(self) -> str:
        return f"{self.idTransaccion} - {self.categoria} - {self.monto}"


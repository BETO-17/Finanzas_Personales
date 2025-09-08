"""Endpoint para actualizar transacciones existentes."""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json

from ..models import Transaccion


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def editar_transaccion(request, id: int):
    """Actualiza los campos enviados en JSON para la transacción indicada.

    Acepta métodos PUT/PATCH. Valida la fecha cuando viene presente.
    """
    try:
        transaccion = Transaccion.objects.get(pk=id)
    except Transaccion.DoesNotExist:
        return JsonResponse({"error": "Transacción no encontrada"}, status=404)

    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    categoria = body.get("categoria")
    fecha_str = body.get("fecha")
    monto = body.get("monto")
    destinatario = body.get("destinatario")
    tipo_transac = body.get("tipo_transac")
    estado_transac = body.get("estado_transac")
    descripcion = body.get("descripcion")

    if categoria is not None:
        transaccion.categoria = categoria
    if fecha_str is not None:
        fecha = parse_date(fecha_str)
        if fecha is None:
            return JsonResponse({"error": "Fecha inválida. Formato esperado YYYY-MM-DD"}, status=400)
        transaccion.fecha = fecha
    if monto is not None:
        transaccion.monto = monto
    if destinatario is not None:
        transaccion.destinatario = destinatario
    if tipo_transac is not None:
        transaccion.tipo_transac = tipo_transac
    if estado_transac is not None:
        transaccion.estado_transac = estado_transac
    if descripcion is not None:
        transaccion.descripcion = descripcion

    transaccion.save()

    return JsonResponse({
        "idTransaccion": transaccion.idTransaccion,
        "categoria": transaccion.categoria,
        "fecha": str(transaccion.fecha),
        "monto": float(transaccion.monto),
        "destinatario": transaccion.destinatario,
        "tipo_transac": transaccion.tipo_transac,
        "estado_transac": transaccion.estado_transac,
        "descripcion": transaccion.descripcion,
    })


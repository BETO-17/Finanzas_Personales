"""Endpoint para crear transacciones.

Recibe un JSON con los campos de Transaccion y crea el registro.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json

from ..models import Transaccion


@csrf_exempt
@require_http_methods(["POST"])
def crear_transaccion(request):
    """Crea una transacción a partir del cuerpo JSON enviado.

    Campos requeridos: categoria, fecha (YYYY-MM-DD), monto, destinatario,
    tipo_transac, estado_transac. "descripcion" es opcional.
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
        categoria = body.get("categoria")
        fecha_str = body.get("fecha")
        monto = body.get("monto")
        destinatario = body.get("destinatario")
        tipo_transac = body.get("tipo_transac")
        estado_transac = body.get("estado_transac")
        descripcion = body.get("descripcion")

        if not all([categoria, fecha_str, monto, destinatario, tipo_transac, estado_transac]):
            return JsonResponse({"error": "Faltan campos obligatorios"}, status=400)

        fecha = parse_date(fecha_str)
        if fecha is None:
            return JsonResponse({"error": "Fecha inválida. Formato esperado YYYY-MM-DD"}, status=400)

        transaccion = Transaccion.objects.create(
            categoria=categoria,
            fecha=fecha,
            monto=monto,
            destinatario=destinatario,
            tipo_transac=tipo_transac,
            estado_transac=estado_transac,
            descripcion=descripcion,
        )

        return JsonResponse({
            "idTransaccion": transaccion.idTransaccion,
            "categoria": transaccion.categoria,
            "fecha": str(transaccion.fecha),
            "monto": float(transaccion.monto),
            "destinatario": transaccion.destinatario,
            "tipo_transac": transaccion.tipo_transac,
            "estado_transac": transaccion.estado_transac,
            "descripcion": transaccion.descripcion,
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as exc:
        return JsonResponse({"error": f"Error al crear: {exc}"}, status=500)
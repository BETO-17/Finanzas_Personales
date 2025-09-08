"""Endpoints de lectura de transacciones (listar y obtener por id)."""
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods

from ..models import Transaccion


@require_http_methods(["GET"])
def listar_transacciones(request):
    """Devuelve un listado JSON de todas las transacciones."""
    transacciones = Transaccion.objects.all()
    data = [
        {
            "idTransaccion": t.idTransaccion,
            "categoria": t.categoria,
            "fecha": str(t.fecha),
            "monto": float(t.monto),
            "destinatario": t.destinatario,
            "tipo_transac": t.tipo_transac,
            "estado_transac": t.estado_transac,
            "descripcion": t.descripcion,
        }
        for t in transacciones
    ]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def obtener_transaccion(request, id: int):
    """Devuelve una transacción por su id o 404 si no existe."""
    try:
        t = Transaccion.objects.get(pk=id)
    except Transaccion.DoesNotExist as exc:
        raise Http404("Transacción no encontrada") from exc

    return JsonResponse({
        "idTransaccion": t.idTransaccion,
        "categoria": t.categoria,
        "fecha": str(t.fecha),
        "monto": float(t.monto),
        "destinatario": t.destinatario,
        "tipo_transac": t.tipo_transac,
        "estado_transac": t.estado_transac,
        "descripcion": t.descripcion,
    })


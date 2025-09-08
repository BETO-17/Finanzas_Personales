"""Endpoint para eliminar transacciones por id."""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ..models import Transaccion


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminar_transaccion(request, id: int):
    """Elimina la transacción indicada. Devuelve 404 si no existe."""
    try:
        transaccion = Transaccion.objects.get(pk=id)
    except Transaccion.DoesNotExist:
        return JsonResponse({"error": "Transacción no encontrada"}, status=404)

    transaccion.delete()
    return JsonResponse({"mensaje": "Transacción eliminada"}, status=200)


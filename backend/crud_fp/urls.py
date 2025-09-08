"""Rutas HTTP para el CRUD de Transaccion.

Se separan las operaciones en archivos dentro de transaccion/.
"""
from django.urls import path
from .transaccion.crear_transac import crear_transaccion
from .transaccion.ver_transac import listar_transacciones, obtener_transaccion
from .transaccion.editar_transac import editar_transaccion
from .transaccion.eliminar_transac import eliminar_transaccion


urlpatterns = [
    path('transacciones/', listar_transacciones, name='listar_transacciones'),
    path('transacciones/crear/', crear_transaccion, name='crear_transaccion'),
    path('transacciones/<int:id>/', obtener_transaccion, name='obtener_transaccion'),
    path('transacciones/<int:id>/editar/', editar_transaccion, name='editar_transaccion'),
    path('transacciones/<int:id>/eliminar/', eliminar_transaccion, name='eliminar_transaccion'),
]


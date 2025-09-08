from django.urls import path
from . import views

app_name = 'crud_fp'

urlpatterns = [
    # URLs para transacciones
    path('transacciones/', views.listar_transacciones, name='listar_transacciones'),
    path('transacciones/json/', views.obtener_transacciones_json, name='transacciones_json'),
    path('transacciones/crear/', views.crear_transaccion, name='crear_transaccion'),
    path('transacciones/<int:transaccion_id>/', views.detalle_transaccion, name='detalle_transaccion'),
    path('transacciones/estadisticas/', views.estadisticas_transacciones, name='estadisticas_transacciones'),
]

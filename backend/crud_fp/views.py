from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json
from .models import Transaccion

def listar_transacciones(request):
    """Vista para listar todas las transacciones con filtros opcionales"""
    transacciones = Transaccion.objects.all()
    
    # Filtros opcionales
    tipo = request.GET.get('tipo')
    categoria = request.GET.get('categoria')
    usuario_id = request.GET.get('usuario')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if tipo:
        transacciones = transacciones.filter(tipo=tipo)
    if categoria:
        transacciones = transacciones.filter(categoria=categoria)
    if usuario_id:
        transacciones = transacciones.filter(usuario_id=usuario_id)
    if fecha_desde:
        transacciones = transacciones.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        transacciones = transacciones.filter(fecha__lte=fecha_hasta)
    
    # Paginación
    paginator = Paginator(transacciones, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calcular totales
    total_ingresos = transacciones.filter(tipo='ingreso').aggregate(Sum('monto'))['monto__sum'] or 0
    total_gastos = transacciones.filter(tipo='gasto').aggregate(Sum('monto'))['monto__sum'] or 0
    balance = total_ingresos - total_gastos
    
    context = {
        'page_obj': page_obj,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'tipos': Transaccion.TIPO_CHOICES,
        'categorias': Transaccion.CATEGORIA_CHOICES,
    }
    
    return render(request, 'transacciones/lista.html', context)

def obtener_transacciones_json(request):
    """API endpoint para obtener transacciones en formato JSON"""
    transacciones = Transaccion.objects.all()
    
    # Aplicar filtros
    tipo = request.GET.get('tipo')
    categoria = request.GET.get('categoria')
    usuario_id = request.GET.get('usuario')
    
    if tipo:
        transacciones = transacciones.filter(tipo=tipo)
    if categoria:
        transacciones = transacciones.filter(categoria=categoria)
    if usuario_id:
        transacciones = transacciones.filter(usuario_id=usuario_id)
    
    # Convertir a lista de diccionarios
    data = []
    for transaccion in transacciones:
        data.append({
            'id': transaccion.id,
            'usuario': transaccion.usuario.username,
            'tipo': transaccion.tipo,
            'tipo_display': transaccion.get_tipo_display(),
            'categoria': transaccion.categoria,
            'categoria_display': transaccion.get_categoria_display(),
            'monto': float(transaccion.monto),
            'descripcion': transaccion.descripcion,
            'fecha': transaccion.fecha.isoformat(),
            'fecha_creacion': transaccion.fecha_creacion.isoformat(),
        })
    
    return JsonResponse({
        'transacciones': data,
        'total': len(data)
    })

def estadisticas_transacciones(request):
    """Vista para mostrar estadísticas de las transacciones"""
    # Estadísticas por tipo
    stats_por_tipo = Transaccion.objects.values('tipo').annotate(
        total=Sum('monto'),
        cantidad=Count('id')
    )
    
    # Estadísticas por categoría
    stats_por_categoria = Transaccion.objects.values('categoria').annotate(
        total=Sum('monto'),
        cantidad=Count('id')
    )
    
    # Estadísticas del último mes
    hace_un_mes = timezone.now() - timedelta(days=30)
    stats_ultimo_mes = Transaccion.objects.filter(fecha__gte=hace_un_mes).aggregate(
        total_ingresos=Sum('monto', filter=Q(tipo='ingreso')),
        total_gastos=Sum('monto', filter=Q(tipo='gasto')),
        cantidad_total=Count('id')
    )
    
    context = {
        'stats_por_tipo': stats_por_tipo,
        'stats_por_categoria': stats_por_categoria,
        'stats_ultimo_mes': stats_ultimo_mes,
    }
    
    return render(request, 'transacciones/estadisticas.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def crear_transaccion(request):
    """API endpoint para crear una nueva transacción"""
    try:
        data = json.loads(request.body)
        
        transaccion = Transaccion.objects.create(
            usuario_id=data['usuario_id'],
            tipo=data['tipo'],
            categoria=data['categoria'],
            monto=data['monto'],
            descripcion=data.get('descripcion', ''),
            fecha=data.get('fecha', timezone.now())
        )
        
        return JsonResponse({
            'success': True,
            'transaccion_id': transaccion.id,
            'message': 'Transacción creada exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def detalle_transaccion(request, transaccion_id):
    """Vista para mostrar el detalle de una transacción específica"""
    transaccion = get_object_or_404(Transaccion, id=transaccion_id)
    
    context = {
        'transaccion': transaccion
    }
    
    return render(request, 'transacciones/detalle.html', context)

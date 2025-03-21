from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from .models import Categoria, Cuenta, Transaccion, Presupuesto, MetasFinancieras
from .forms import (
    CategoriaForm, CuentaForm, TransaccionForm,
    PresupuestoForm, MetasFinancierasForm
)
import calendar

@login_required
def home(request):
    """Vista principal del dashboard"""
    # Obtener resumen de cuentas
    cuentas = Cuenta.objects.filter(usuario=request.user)
    total_saldo = cuentas.aggregate(total=Sum('saldo'))['total'] or Decimal('0')

    # Obtener últimas transacciones
    ultimas_transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')[:5]

    # Obtener resumen de gastos por categoría
    gastos_categoria = Transaccion.objects.filter(
        usuario=request.user,
        tipo='gasto',
        fecha__month=timezone.now().month
    ).values('categoria__nombre').annotate(
        total=Sum('monto'),
        count=Count('id')
    ).order_by('-total')

    # Calcular total de gastos del mes actual
    total_gastos = Transaccion.objects.filter(
        usuario=request.user,
        tipo='gasto',
        fecha__month=timezone.now().month
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0')

    # Obtener metas financieras activas
    metas_activas = MetasFinancieras.objects.filter(
        usuario=request.user,
        estado='en_progreso'
    ).order_by('fecha_objetivo')

    context = {
        'cuentas': cuentas,
        'total_saldo': total_saldo,
        'ultimas_transacciones': ultimas_transacciones,
        'gastos_categoria': gastos_categoria,
        'metas_activas': metas_activas,
        'total_gastos': total_gastos,
    }
    return render(request, 'core/home.html', context)

@login_required
def categorias(request):
    """Gestión de categorías"""
    categorias = Categoria.objects.filter(usuario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categorias')
    else:
        form = CategoriaForm()
    
    context = {
        'categorias': categorias,
        'form': form,
    }
    return render(request, 'core/categorias.html', context)

@login_required
def cuentas(request):
    """Gestión de cuentas"""
    cuentas = Cuenta.objects.filter(usuario=request.user)
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            cuenta = form.save(commit=False)
            cuenta.usuario = request.user
            cuenta.save()
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('cuentas')
    else:
        form = CuentaForm()
    
    context = {
        'cuentas': cuentas,
        'form': form,
    }
    return render(request, 'core/cuentas.html', context)

@login_required
def transacciones(request):
    """Gestión de transacciones"""
    transacciones = Transaccion.objects.filter(usuario=request.user).order_by('-fecha')
    if request.method == 'POST':
        form = TransaccionForm(request.POST, user=request.user)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.usuario = request.user
            transaccion.save()
            messages.success(request, 'Transacción registrada exitosamente.')
            return redirect('transacciones')
    else:
        form = TransaccionForm(user=request.user)
    
    context = {
        'transacciones': transacciones,
        'form': form,
    }
    return render(request, 'core/transacciones.html', context)

@login_required
def presupuestos(request):
    """Gestión de presupuestos"""
    presupuestos = Presupuesto.objects.filter(usuario=request.user)
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, user=request.user)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.save()
            messages.success(request, 'Presupuesto creado exitosamente.')
            return redirect('presupuestos')
    else:
        form = PresupuestoForm(user=request.user)
    
    context = {
        'presupuestos': presupuestos,
        'form': form,
    }
    return render(request, 'core/presupuestos.html', context)

@login_required
def metas_financieras(request):
    """Gestión de metas financieras"""
    metas = MetasFinancieras.objects.filter(usuario=request.user)
    if request.method == 'POST':
        form = MetasFinancierasForm(request.POST)
        if form.is_valid():
            meta = form.save(commit=False)
            meta.usuario = request.user
            meta.save()
            messages.success(request, 'Meta financiera creada exitosamente.')
            return redirect('metas_financieras')
    else:
        form = MetasFinancierasForm()
    
    context = {
        'metas': metas,
        'form': form,
    }
    return render(request, 'core/metas_financieras.html', context)

@login_required
def reportes(request):
    """Vista de reportes y análisis"""
    # Obtener fechas para el filtro
    fecha_inicio = request.GET.get('fecha_inicio', (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_fin = request.GET.get('fecha_fin', timezone.now().strftime('%Y-%m-%d'))

    # Filtrar transacciones por fecha
    transacciones = Transaccion.objects.filter(
        usuario=request.user,
        fecha__range=[fecha_inicio, fecha_fin]
    )

    # Calcular totales
    total_ingresos = transacciones.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total'] or Decimal('0')
    total_gastos = transacciones.filter(tipo='gasto').aggregate(total=Sum('monto'))['total'] or Decimal('0')
    balance = total_ingresos - total_gastos

    # Agrupar por categoría
    gastos_categoria = transacciones.filter(tipo='gasto').values(
        'categoria__nombre'
    ).annotate(
        total=Sum('monto'),
        count=Count('id')
    ).order_by('-total')

    context = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': balance,
        'gastos_categoria': gastos_categoria,
    }
    return render(request, 'core/reportes.html', context)

def editar_cuenta(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta actualizada exitosamente.')
            return redirect('cuentas')
    else:
        form = CuentaForm(instance=cuenta)
    return render(request, 'core/cuentas.html', {'form': form})

def eliminar_cuenta(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk, usuario=request.user)
    if request.method == 'POST':
        cuenta.delete()
        messages.success(request, 'Cuenta eliminada exitosamente.')
        return redirect('cuentas')
    return render(request, 'core/confirmar_eliminacion.html', {
        'objeto': cuenta,
        'tipo': 'cuenta'
    })

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'core/categorias.html', {'form': form})

@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('categorias')
    return render(request, 'core/confirmar_eliminacion.html', {
        'objeto': categoria,
        'tipo': 'categoría'
    })

@login_required
def editar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, instance=presupuesto, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Presupuesto actualizado exitosamente.')
            return redirect('presupuestos')
    else:
        form = PresupuestoForm(instance=presupuesto, user=request.user)
    return render(request, 'core/editar_presupuesto.html', {'form': form, 'presupuesto': presupuesto})

@login_required
def eliminar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        presupuesto.delete()
        messages.success(request, 'Presupuesto eliminado exitosamente.')
        return redirect('presupuestos')
    return render(request, 'core/confirmar_eliminacion.html', {
        'objeto': presupuesto,
        'tipo': 'presupuesto',
        'url_cancelar': 'presupuestos'
    })

@login_required
def tarjetas_credito(request):
    # Obtener las tarjetas de crédito del usuario
    tarjetas = Cuenta.objects.filter(usuario=request.user, tipo='tarjeta_credito')
    print("Tarjetas encontradas:", tarjetas)
    
    # Obtener el mes y año actual
    hoy = timezone.now().date()
    print("Fecha actual:", hoy)
    
    # Generar los próximos 12 meses
    meses = []
    for i in range(12):
        fecha = hoy + timedelta(days=30*i)
        meses.append({
            'nombre': calendar.month_name[fecha.month],
            'año': fecha.year,
            'mes': fecha.month
        })
    print("Meses generados:", meses)
    
    # Calcular los pagos estimados por tarjeta y mes
    pagos_estimados = []
    for tarjeta in tarjetas:
        pagos_tarjeta = {
            'tarjeta': tarjeta,
            'meses': {}
        }
        
        # Inicializar todos los meses en 0
        for mes in meses:
            key = f"{mes['mes']}_{mes['año']}"
            pagos_tarjeta['meses'][key] = Decimal('0')
        
        # Obtener todas las transacciones de la tarjeta que tienen cuotas
        transacciones = Transaccion.objects.filter(
            usuario=request.user,
            cuenta=tarjeta,
            tipo='gasto',
            cuotas__gt=1
        )
        print(f"\nTransacciones para tarjeta {tarjeta.nombre}:")
        
        # Para cada transacción, calcular sus cuotas futuras
        for transaccion in transacciones:
            print(f"Procesando transacción: {transaccion.descripcion}")
            print(f"- Monto: {transaccion.monto}")
            print(f"- Cuotas totales: {transaccion.cuotas}")
            print(f"- Cuota actual: {transaccion.cuota_actual}")
            print(f"- Fecha vencimiento: {transaccion.fecha_vencimiento}")
            
            # Calcular el monto de cada cuota
            monto_cuota = transaccion.monto / transaccion.cuotas
            
            # Determinar la fecha de inicio para las cuotas
            fecha_inicio = transaccion.fecha_vencimiento or transaccion.fecha
            if hasattr(fecha_inicio, 'date'):
                fecha_inicio = fecha_inicio.date()
            
            # Calcular las cuotas restantes
            cuotas_restantes = transaccion.cuotas - transaccion.cuota_actual + 1
            
            # Distribuir las cuotas en los meses correspondientes
            for i in range(cuotas_restantes):
                fecha_cuota = fecha_inicio + timedelta(days=30*i)
                key = f"{fecha_cuota.month}_{fecha_cuota.year}"
                
                # Solo agregar si el mes está en nuestro rango de 12 meses
                for mes in meses:
                    if mes['mes'] == fecha_cuota.month and mes['año'] == fecha_cuota.year:
                        pagos_tarjeta['meses'][key] += monto_cuota
                        print(f"Agregando cuota de {monto_cuota} para {key}")
                        break
        
        pagos_estimados.append(pagos_tarjeta)
    
    context = {
        'tarjetas': tarjetas,
        'meses': meses,
        'pagos_estimados': pagos_estimados,
    }
    return render(request, 'core/tarjetas_credito.html', context)

@login_required
def editar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción actualizada exitosamente.')
            return redirect('transacciones')
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'core/editar_transaccion.html', {
        'form': form,
        'transaccion': transaccion,
        'url_cancelar': 'transacciones'
    })

@login_required
def eliminar_transaccion(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, 'Transacción eliminada exitosamente.')
        return redirect('transacciones')
    return render(request, 'core/confirmar_eliminacion.html', {
        'objeto': transaccion,
        'url_cancelar': 'transacciones'
    })

@login_required
def editar_meta(request, pk):
    meta = get_object_or_404(MetasFinancieras, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = MetasFinancierasForm(request.POST, instance=meta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meta financiera actualizada exitosamente.')
            return redirect('metas_financieras')
    else:
        form = MetasFinancierasForm(instance=meta)
    return render(request, 'core/editar_meta.html', {'form': form, 'meta': meta})

@login_required
def eliminar_meta(request, pk):
    meta = get_object_or_404(MetasFinancieras, pk=pk, usuario=request.user)
    if request.method == 'POST':
        meta.delete()
        messages.success(request, 'Meta financiera eliminada exitosamente.')
        return redirect('metas_financieras')
    return render(request, 'core/confirmar_eliminacion.html', {
        'objeto': meta,
        'tipo': 'meta financiera'
    })

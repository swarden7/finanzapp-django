from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categorias/', views.categorias, name='categorias'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('cuentas/', views.cuentas, name='cuentas'),
    path('cuentas/editar/<int:pk>/', views.editar_cuenta, name='editar_cuenta'),
    path('cuentas/eliminar/<int:pk>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('transacciones/editar/<int:pk>/', views.editar_transaccion, name='editar_transaccion'),
    path('transacciones/eliminar/<int:pk>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    path('presupuestos/', views.presupuestos, name='presupuestos'),
    path('presupuestos/editar/<int:pk>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/eliminar/<int:pk>/', views.eliminar_presupuesto, name='eliminar_presupuesto'),
    path('metas_financieras/', views.metas_financieras, name='metas_financieras'),
    path('metas/editar/<int:pk>/', views.editar_meta, name='editar_meta'),
    path('metas/eliminar/<int:pk>/', views.eliminar_meta, name='eliminar_meta'),
    path('reportes/', views.reportes, name='reportes'),
    path('tarjetas_credito/', views.tarjetas_credito, name='tarjetas_credito'),
] 
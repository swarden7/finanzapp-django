from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=[
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ])
    color = models.CharField(max_length=7, default='#000000')
    icono = models.CharField(max_length=50, default='fas fa-money-bill')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class Cuenta(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[
        ('efectivo', 'Efectivo'),
        ('cuenta_corriente', 'Cuenta Corriente'),
        ('cuenta_ahorro', 'Cuenta de Ahorro'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('otro', 'Otro'),
    ])
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    moneda = models.CharField(max_length=3, default='CLP')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class Transaccion(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=20, choices=[
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ])
    cuotas = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    cuota_actual = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    fecha_vencimiento = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha', '-created_at']

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.monto} - {self.descripcion}"

    def save(self, *args, **kwargs):
        # Actualizar el saldo de la cuenta solo si no es una tarjeta de crédito
        cuenta = self.cuenta
        if cuenta.tipo != 'tarjeta_credito':
            if self.tipo == 'ingreso':
                cuenta.saldo += self.monto
            else:
                cuenta.saldo -= self.monto
            cuenta.save()
        super().save(*args, **kwargs)

    @property
    def monto_cuota(self):
        """Calcula el monto de cada cuota"""
        return self.monto / self.cuotas

    @property
    def es_ultima_cuota(self):
        """Verifica si es la última cuota"""
        return self.cuota_actual == self.cuotas

    @property
    def saldo_pendiente(self):
        """Calcula el saldo pendiente de la transacción"""
        return self.monto - (self.monto_cuota * (self.cuota_actual - 1))

class Presupuesto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    periodo = models.CharField(max_length=20, choices=[
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
        ('personalizado', 'Personalizado'),
    ])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Presupuesto {self.categoria.nombre} - {self.get_periodo_display()}"

class MetasFinancieras(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    monto_objetivo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    monto_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_objetivo = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], default='en_progreso')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Meta Financiera'
        verbose_name_plural = 'Metas Financieras'
        ordering = ['-fecha_objetivo']

    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"

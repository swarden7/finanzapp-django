# Generated by Django 5.0.7 on 2025-03-18 15:18

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("descripcion", models.TextField(blank=True)),
                (
                    "tipo",
                    models.CharField(
                        choices=[("ingreso", "Ingreso"), ("gasto", "Gasto")],
                        max_length=20,
                    ),
                ),
                ("color", models.CharField(default="#000000", max_length=7)),
                ("icono", models.CharField(default="fas fa-money-bill", max_length=50)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Categoría",
                "verbose_name_plural": "Categorías",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="Cuenta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                (
                    "tipo",
                    models.CharField(
                        choices=[
                            ("efectivo", "Efectivo"),
                            ("cuenta_corriente", "Cuenta Corriente"),
                            ("cuenta_ahorro", "Cuenta de Ahorro"),
                            ("tarjeta_credito", "Tarjeta de Crédito"),
                            ("tarjeta_debito", "Tarjeta de Débito"),
                            ("otro", "Otro"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "saldo",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                ("moneda", models.CharField(default="CLP", max_length=3)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Cuenta",
                "verbose_name_plural": "Cuentas",
                "ordering": ["nombre"],
            },
        ),
        migrations.CreateModel(
            name="MetasFinancieras",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("descripcion", models.TextField()),
                (
                    "monto_objetivo",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                (
                    "monto_actual",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                ("fecha_objetivo", models.DateField()),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("en_progreso", "En Progreso"),
                            ("completada", "Completada"),
                            ("cancelada", "Cancelada"),
                        ],
                        default="en_progreso",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Meta Financiera",
                "verbose_name_plural": "Metas Financieras",
                "ordering": ["-fecha_objetivo"],
            },
        ),
        migrations.CreateModel(
            name="Presupuesto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "monto",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                (
                    "periodo",
                    models.CharField(
                        choices=[
                            ("mensual", "Mensual"),
                            ("anual", "Anual"),
                            ("personalizado", "Personalizado"),
                        ],
                        max_length=20,
                    ),
                ),
                ("fecha_inicio", models.DateField()),
                ("fecha_fin", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.categoria"
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Presupuesto",
                "verbose_name_plural": "Presupuestos",
                "ordering": ["-fecha_inicio"],
            },
        ),
        migrations.CreateModel(
            name="Transaccion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha", models.DateField()),
                (
                    "monto",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                ("descripcion", models.TextField()),
                (
                    "tipo",
                    models.CharField(
                        choices=[("ingreso", "Ingreso"), ("gasto", "Gasto")],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.categoria"
                    ),
                ),
                (
                    "cuenta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.cuenta"
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Transacción",
                "verbose_name_plural": "Transacciones",
                "ordering": ["-fecha", "-created_at"],
            },
        ),
    ]

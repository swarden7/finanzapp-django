# FinanzApp - Sistema de Gestión Financiera Personal

FinanzApp es una aplicación web desarrollada con Django que permite gestionar tus finanzas personales de manera eficiente y organizada. La aplicación incluye funcionalidades para el seguimiento de gastos, ingresos, presupuestos, metas financieras y tarjetas de crédito.

## Características Principales

- **Gestión de Transacciones**
  - Registro de ingresos y gastos
  - Categorización de transacciones
  - Sistema de cuotas para tarjetas de crédito
  - Historial detallado de transacciones

- **Gestión de Cuentas**
  - Múltiples tipos de cuentas (efectivo, cuenta corriente, tarjeta de crédito, etc.)
  - Seguimiento de saldos
  - Moneda personalizable

- **Presupuestos**
  - Creación de presupuestos por categoría
  - Períodos personalizables (mensual, anual, personalizado)
  - Seguimiento de gastos vs presupuesto

- **Metas Financieras**
  - Definición de objetivos financieros
  - Seguimiento de progreso
  - Estados de avance (en progreso, completada, cancelada)

- **Tarjetas de Crédito**
  - Gestión de compras a cuotas
  - Visualización de pagos futuros
  - Seguimiento de cuotas pendientes

## Requisitos del Sistema

- Python 3.8 o superior
- Django 5.0.7
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/swarden7/finanzapp-django.git
cd finanzapp-django
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
   - Copiar `.env.example` a `.env`
   - Ajustar las variables según sea necesario

5. Realizar migraciones:
```bash
python manage.py migrate
```

6. Crear un superusuario:
```bash
python manage.py createsuperuser
```

7. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
finanzapp/
├── core/               # Aplicación principal
│   ├── models.py      # Modelos de datos
│   ├── views.py       # Vistas y lógica de negocio
│   ├── forms.py       # Formularios
│   └── urls.py        # Rutas de la aplicación
├── templates/         # Plantillas HTML
├── static/           # Archivos estáticos
├── media/            # Archivos subidos por usuarios
└── manage.py         # Script de gestión de Django
```

## Tecnologías Utilizadas

- Django 5.0.7
- Python-dotenv para gestión de variables de entorno
- Django Crispy Forms para formularios estilizados
- Bootstrap 5 para el diseño frontend
- Pillow para manejo de imágenes
- Django Filter para filtrado de datos
- Django Widget Tweaks para personalización de widgets

## Contribuir

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un Fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Alejandro Heredia - [@swarden7](https://github.com/swarden7)

Link del Proyecto: [https://github.com/swarden7/finanzapp-django](https://github.com/swarden7/finanzapp-django) 
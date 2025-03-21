from django import template

register = template.Library()

@register.filter
def format_money(value):
    """Formatea un monto de dinero con el formato $XX.XXX"""
    try:
        # Convertir a entero y formatear con separador de miles
        return f"${int(float(value)):,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$0" 
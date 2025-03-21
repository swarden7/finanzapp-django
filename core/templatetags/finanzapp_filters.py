from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def div(value, arg):
    """Divide el valor por el argumento"""
    try:
        return Decimal(str(value)) / Decimal(str(arg))
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    """Multiplica el valor por el argumento"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return 0

@register.filter
def get_item(dictionary, key):
    """Obtiene un valor del diccionario por su clave"""
    try:
        return dictionary.get(key, Decimal('0'))
    except (AttributeError, TypeError):
        return Decimal('0') 
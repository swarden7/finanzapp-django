from django import forms
from .models import Categoria, Cuenta, Transaccion, Presupuesto, MetasFinancieras
from django.utils import timezone

ICON_CHOICES = [
    ('fas fa-money-bill', 'Dinero'),
    ('fas fa-shopping-cart', 'Compras'),
    ('fas fa-utensils', 'Comida'),
    ('fas fa-home', 'Hogar'),
    ('fas fa-car', 'Transporte'),
    ('fas fa-heart', 'Salud'),
    ('fas fa-graduation-cap', 'Educación'),
    ('fas fa-gamepad', 'Entretenimiento'),
    ('fas fa-tshirt', 'Ropa'),
    ('fas fa-wifi', 'Servicios'),
    ('fas fa-gift', 'Regalos'),
    ('fas fa-piggy-bank', 'Ahorro'),
    ('fas fa-coins', 'Inversiones'),
    ('fas fa-hand-holding-usd', 'Ingresos'),
    ('fas fa-file-invoice-dollar', 'Facturas'),
]

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'tipo', 'color', 'icono']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'icono': forms.Select(choices=ICON_CHOICES, attrs={
                'class': 'mt-1 block w-full pl-10 pr-3 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md'
            }),
        }

class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['nombre', 'tipo', 'saldo', 'moneda']
        widgets = {
            'saldo': forms.NumberInput(attrs={'step': '0.01'}),
        }

class TransaccionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.user)
            self.fields['cuenta'].queryset = Cuenta.objects.filter(usuario=self.user)
        self.fields['cuota_actual'].initial = 1
        self.fields['cuotas'].initial = 1

    class Meta:
        model = Transaccion
        fields = ['fecha', 'monto', 'descripcion', 'categoria', 'cuenta', 'tipo', 'cuotas', 'cuota_actual', 'fecha_vencimiento']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'monto': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'categoria': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'cuenta': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'tipo': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
            'cuotas': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm', 'min': '1'}),
            'cuota_actual': forms.NumberInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm', 'min': '1'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'}),
        }

class PresupuestoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.user)

    class Meta:
        model = Presupuesto
        fields = ['categoria', 'monto', 'periodo', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'monto': forms.NumberInput(attrs={'step': '0.01'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        periodo = cleaned_data.get('periodo')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if periodo == 'personalizado' and not fecha_fin:
            raise forms.ValidationError('La fecha de fin es requerida para presupuestos personalizados.')

        if fecha_fin and fecha_fin < fecha_inicio:
            raise forms.ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

        return cleaned_data

class MetasFinancierasForm(forms.ModelForm):
    class Meta:
        model = MetasFinancieras
        fields = ['nombre', 'descripcion', 'monto_objetivo', 'fecha_objetivo', 'estado']
        widgets = {
            'monto_objetivo': forms.NumberInput(attrs={'step': '0.01'}),
            'fecha_objetivo': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_objetivo = cleaned_data.get('fecha_objetivo')
        estado = cleaned_data.get('estado')

        if fecha_objetivo and fecha_objetivo < timezone.now().date():
            if estado == 'en_progreso':
                raise forms.ValidationError('No se puede crear una meta en progreso con fecha objetivo pasada.')

        return cleaned_data 
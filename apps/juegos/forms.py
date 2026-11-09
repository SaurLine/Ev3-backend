from django import forms
from .models import Videojuego

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = [
            'genero', 'codigo', 'titulo', 'descripcion', 
            'desarrollador', 'precio', 'plataforma', 
            'stock', 'estado', 'imagen', 'activo'
        ]
        widgets = {
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ACC-001'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del videojuego'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción detallada...'}),
            'desarrollador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estudio desarrollador'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'plataforma': forms.Select(attrs={'class': 'form-select'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo').upper()
        queryset = Videojuego.objects.filter(codigo=codigo)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError("Ya existe otro videojuego registrado con este código identificador.")
        return codigo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError("El precio no puede ser un valor negativo.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock disponible no puede ser negativo.")
        return stock
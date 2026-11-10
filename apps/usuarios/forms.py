from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirmar Contraseña")
    

    rut = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name'] 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirmar_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            
            PerfilUsuario.objects.create(
                user=user,
                rut=self.cleaned_data["rut"],
                telefono=self.cleaned_data["telefono"],
                rol_institucional=PerfilUsuario.RolInstitucional.ESTANDAR
            )
        return user
from django import forms
from .models import producto, user, bolsa, carro, boleta


class ProductoForm(forms.ModelForm):
    class Meta:
        model = producto
        fields = '__all__'

#Para crear usuario
class UserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = '__all__'

# Para acceder
class LoginForm(forms.Form):
    user_name = forms.CharField(max_length=45, label='Nombre de usuario', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')
 
# Para producto y cantidad
class BolsaForm(forms.ModelForm):
    class Meta:
        model = bolsa
        fields = '__all__'

# Para el carrito de compras
class CarroForm(forms.ModelForm):
    class Meta:
        model = carro
        fields = '__all__'

# Para el pago
class BoletaForm(forms.ModelForm):
    class Meta:
        model = boleta
        fields = '__all__'

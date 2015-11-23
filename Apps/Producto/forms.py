# encoding utf-8
from django import forms
from .models import Producto, Marca


class CrearProductoForm(forms.ModelForm):
    # codigo = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control',}))
    # descripcion = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control', \
    #                               'placeholder': 'Codigo de barras'}))
    # p_unitario = forms.DecimalField(widget = forms.NumberInput(attrs={'class':'form-control',}))
    # p_mayoreo = forms.DecimalField(widget = forms.NumberInput(attrs={'class':'form-control',}))
    # inventario = forms.BooleanField(widget = forms.CheckboxInput(attrs={'class':'form-control',}))
    # cantidad = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control',}))
    # minimo = forms.IntegerField(widget = forms.NumberInput(attrs={'class':'form-control'},))

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            # 'code39': forms.CheckboxInput(attrs={'class': 'xxd', }),
            'codigo': forms.TextInput(attrs={'class': 'form-control', }),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', }),
            'marca': forms.Select(attrs={'class': 'form-control', }),
            'punitario': forms.NumberInput(attrs={'class': 'form-control', }),
            'pmayoreo': forms.NumberInput(attrs={'class': 'form-control', }),
            # 'vunidad': forms.CheckboxInput(attrs={'class': 'pull-right', }),
            # 'inventario': forms.CheckboxInput(attrs={'class': 'pull-left', }),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', }),
            'minimo': forms.NumberInput(attrs={'class': 'form-control', }),
        }


class CrearMarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', }),
        }

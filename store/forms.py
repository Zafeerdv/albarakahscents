from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, ProductImage

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'size', 'price', 'original_price', 'discount_price', 'stock']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'position']
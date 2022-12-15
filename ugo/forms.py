from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super(LoginForm, self)._init_(*args, **kwargs)   
    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }    
    

     
        

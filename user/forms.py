from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class UserForm(forms.ModelForm):
    def _init_(self, *args, **kwargs):
        self.fields['estado'].widget.attrs.update({'class': 'form-control' })
        super(UserForm, self)._init_(*args, **kwargs)
    class Meta:
        model = Usuario
        exclude = ['last_login', 'is_superuser', 'username', 'first_name', 
        'last_name', 'is_staff', 'is_active', 'date_joined', 'created_at', 
        'groups', 'user_permissions', 'update_at']
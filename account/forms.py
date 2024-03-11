from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, ValidationError, UserCreationForm
from .models import User
class UserCreationForm2(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'password1', 'password2', 'nid', "phone"]
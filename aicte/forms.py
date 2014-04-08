from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class UserRegisterForm(UserCreationForm):

        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
                            

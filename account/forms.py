from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Add avalid email address')

    class Meta:
        model = User
        fields = ('email', 'username', 'family', 'password1', 'password2', 'role')


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError('invalid Login!')

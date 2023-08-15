from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm 

class loginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", 'placeholder': 'xyz'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", 'placeholder': '********'}))
    
      
      
class signupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'xyz'}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '********'}))
    password2 = forms.CharField(label="Retype password",widget=forms.PasswordInput(attrs={"class": "form-control", 'placeholder': '********'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'xyz@email.com'}))
    IS_OWNER_CHOICES = (
        (True, "Owner"),
        (False, "Customer"),
    )
    is_owner = forms.ChoiceField(
        label="Account Type",
        choices=IS_OWNER_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_owner")

          
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import CustomUser


class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.Textarea()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'city', 'description')

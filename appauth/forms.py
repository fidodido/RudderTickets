from django import forms

class AuthForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'login-input form-control'}))
    password = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'login-input form-control'}))

from django import forms

class LoginForm(forms.Form):
    contact = forms.CharField(max_length=255, label="Phone Number or Email", required=True)

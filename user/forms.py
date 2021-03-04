from django import forms
from django.forms import ModelForm

from core.models import User


class UserForm(ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                "password and password_confirm does not match"
            )
        return cleaned_data

    class Meta:
        model = User
        fields = '__all__'

# my_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Your passwords must match")

        # Custom password validation
        if len(password1) < 5:
            raise forms.ValidationError("This password is too short. It must contain at least 8 characters.")
        if password1.isdigit():
            raise forms.ValidationError("This password is entirely numeric.")
        if password1.lower() in ['password', '12345678', 'qwerty']:
            raise forms.ValidationError("This password is too common.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.set_password(self.cleaned_data["password1"])
            user.save()
        return user
# my_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise forms.ValidationError("This field is required.")
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already in use.")
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
    
        if not email:
            raise forms.ValidationError("This field is required.")
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("This email is invalid.")
        
        return email
    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password1 :
            raise forms.ValidationError("This field is required.")
        
        if not password2:
            raise forms.ValidationError("Verify password.")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Your passwords must match")    
        
        if(len(password1) < 5):
            raise forms.ValidationError("Password too short")
        
        if(len(password1) > 20):
            raise forms.ValidationError("Password too long")
        
        return password2
    
    def clean(self):
        cleaned_data = super().clean()
        self.clean_password2()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.set_password(self.cleaned_data["password1"])
            user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")
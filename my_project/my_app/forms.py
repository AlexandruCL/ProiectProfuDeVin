# my_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Order
from django.contrib.auth.forms import SetPasswordForm
from .validators import validate_password_strength

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
        
        validate_password_strength(password2)
        

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

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError("Both fields required.")

        user = authenticate(username=username, password=password)
        if not user:
            try:
                user_temp = User.objects.get(email=username)
                user = authenticate(username=user_temp.username, password=password)
                if not user:
                    raise forms.ValidationError("Invalid credentials")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid credentials")

        self.user_cache = user
        return self.cleaned_data
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name','email', 'phone_number', 'address', 'city', 'county', 'postal_code']
    
    def clean_county(self):
        county = self.cleaned_data.get("county")
        
        if not county:
            raise forms.ValidationError("This field is required.")
        
        if not county.isalpha():
            raise forms.ValidationError("Ivalid county.")
        
        return county
    def clean_city(self):
        city = self.cleaned_data.get("city")
        
        if not city:
            raise forms.ValidationError("This field is required.")
        
        if not city.isalpha():
            raise forms.ValidationError("Ivalid city.")
        
        return city
    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code")
        
        if not postal_code:
            raise forms.ValidationError("This field is required.")
        
        if len(postal_code) < 6:
            raise forms.ValidationError("Ivalid postal code.")
        
        if len(postal_code) > 6:
            raise forms.ValidationError("Ivalid postal code.")
        
        if not postal_code.isnumeric():
            raise forms.ValidationError("Ivalid postal code.")
        
        return postal_code
    def clean_address(self):
        address = self.cleaned_data.get("address")
        
        if not address:
            raise forms.ValidationError("This field is required.")
        
        return address
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        
        if not last_name:
            raise forms.ValidationError("This field is required.")
        
        if not last_name.isalpha():
            raise forms.ValidationError("Ivalid last name.")
        
        return last_name
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        
        if not first_name:
            raise forms.ValidationError("This field is required.")
        
        if not first_name.isalpha():
            raise forms.ValidationError("Ivalid first name.")
        
        return first_name
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        
        if not phone_number:
            raise forms.ValidationError("This field is required.")
        
        if len(phone_number) < 10:
            raise forms.ValidationError("Ivalid phone number.")
        
        if len(phone_number) > 10:
            raise forms.ValidationError("Ivalid phone number.")
        
        if not phone_number.isnumeric():
            raise forms.ValidationError("Ivalid phone number.")
        
        return phone_number
    def clean_emailorder(self):
        email = self.cleaned_data.get("email")
    
        if not email:
            raise forms.ValidationError("This field is required.")
        
        
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("This email is invalid.")
        
        return email
    
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full py-4 pl-10 pr-4 text-black placeholder-gray-500 transition-all duration-200 bg-white border border-gray-200 rounded-md focus:outline-none focus:border-blue-600 caret-blue-600',
            'placeholder': 'Enter new password'
        }),
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full py-4 pl-10 pr-4 text-black placeholder-gray-500 transition-all duration-200 bg-white border border-gray-200 rounded-md focus:outline-none focus:border-blue-600 caret-blue-600',
            'placeholder': 'Confirm new password'
        }),
    )    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")

        if not password1:
            raise forms.ValidationError("This field is required.")
        
        if not password2:
            raise forms.ValidationError("Verify password.")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Your passwords must match")    
        
        validate_password_strength(password1)

        return password2
    

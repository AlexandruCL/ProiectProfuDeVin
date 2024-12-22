from django.core.exceptions import ValidationError

def validate_password_strength(password):
    if len(password) < 8:
        raise ValidationError("Password too short")
    if password.count(" ") > 0:
        raise ValidationError("Invalid password")
    if password.isdigit():
        raise ValidationError("Invalid password")
    if password.isalpha():
        raise ValidationError("Invalid password")
    if password.islower():
        raise ValidationError("Invalid password")
    if not any(char in "@#$%^&*" for char in password):
        raise ValidationError("Invalid password")
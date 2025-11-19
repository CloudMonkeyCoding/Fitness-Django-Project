from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import StudentProfile

class StudentSignupForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Full name",
        })
    )
    age = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            "placeholder": "Age",
        })
    )
    section = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            "placeholder": "Section (e.g. 10-A)",
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
        })
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def save(self):
        data = self.cleaned_data

        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
        )

        profile = StudentProfile.objects.create(
            user=user,
            full_name=data["full_name"],
            age=data["age"],
            section=data["section"],
        )
        return user, profile
    
class StudentLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Name / Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            cleaned_data["user"] = user

        return cleaned_data
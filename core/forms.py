from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import FitnessTestEntry, StudentProfile

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


class PreTestForm(forms.Form):
    height_cm = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("1"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="Height (cm)",
    )
    weight_kg = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("1"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="Weight (kg)",
    )
    vo2_max = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="VO₂ Max",
    )
    flexibility = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="Flexibility",
        help_text="Measured in centimeters",
    )
    strength = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="Strength",
        help_text="Number of push-ups",
    )
    agility = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="Agility",
    )
    speed = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="Speed",
    )
    endurance = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(attrs={"step": "1"}),
        label="Endurance",
    )

    def clean(self):
        cleaned_data = super().clean()

        height_cm = cleaned_data.get("height_cm")
        weight_kg = cleaned_data.get("weight_kg")

        if height_cm and weight_kg:
            try:
                height_m = Decimal(height_cm) / Decimal("100")
                if height_m <= 0:
                    raise forms.ValidationError("Height must be greater than zero.")
                bmi = (Decimal(weight_kg) / (height_m ** 2)).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                cleaned_data["bmi"] = bmi
            except (InvalidOperation, ZeroDivisionError):
                raise forms.ValidationError("Unable to calculate BMI from the provided values.")

        return cleaned_data

    def save(self, student: StudentProfile) -> FitnessTestEntry:
        data = self.cleaned_data

        return FitnessTestEntry.objects.create(
            student=student,
            test_type=FitnessTestEntry.PRETEST,
            bmi=data["bmi"],
            vo2_max=data["vo2_max"],
            flexibility=data["flexibility"],
            strength=data["strength"],
            agility=data["agility"],
            speed=data["speed"],
            endurance=data["endurance"],
        )

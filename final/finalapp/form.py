from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta


class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter  User name'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter  Email id'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter  Password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter  Confirm password'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Phone number'
    }), validators=[RegexValidator(r'^\d{10,15}$', message="Enter a valid phone number.")])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1',
                  'password2', 'phone_number']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widgets or other form attributes if needed


class HiringForm(forms.ModelForm):
    class Meta:
        model = Hiring

        fields = [
            'manager_name',
            'event_date',
            'start_time',
            'end_time',
            'total_members',
            'event_location',
            'building_name',
        ]

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        today = date.today()
        three_months_later = today + timedelta(days=90)

        if event_date < today or event_date > three_months_later:
            raise ValidationError(
                'Date should not be in the past and should be within 3 months from today.'
            )

        return event_date

    """ def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        max_allowed_difference = timedelta(hours=5)

        if end_time - start_time > max_allowed_difference:
            raise ValidationError(
                'Time difference should be less than or equal to 5 hours.')

        min_time = datetime.strptime('04:00', '%H:%M').time()
        max_time = datetime.strptime('22:00', '%H:%M').time()

        if start_time < min_time or end_time > max_time:
            raise ValidationError(
                'Start and end time should be between 4:00 AM and 10:00 PM.')

        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        start_time = self.cleaned_data['start_time']
        max_allowed_difference = timedelta(hours=5)

        if end_time - start_time > max_allowed_difference:
            raise ValidationError(
                'Time difference should be less than or equal to 5 hours.')

        min_time = datetime.strptime('04:00', '%H:%M').time()
        max_time = datetime.strptime('22:00', '%H:%M').time()

        if end_time < min_time or end_time > max_time:
            raise ValidationError(
                'End time should be between 4:00 AM and 10:00 PM.')

        return end_time """

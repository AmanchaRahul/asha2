from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SkinCareCheck

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    full_name = forms.CharField(max_length=150, required=True, help_text='Required. Enter your full name.')

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']  # Using first_name to store full name
        if commit:
            user.save()
        return user
    
    
    

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    topic = forms.ChoiceField(choices=[
        ('', 'Select a topic'),
        ('diabetes', 'Diabetes'),
        ('blood_pressure', 'Blood Pressure'),
        ('skincare', 'Skincare'),
        ('other', 'Other')
    ], required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    
    
    
    


class SkinCareCheckForm(forms.ModelForm):
    class Meta:
        model = SkinCareCheck
        fields = ['skin_type', 'concerns']
        widgets = {
            'concerns': forms.Textarea(attrs={'rows': 3}),
        }


class OTPLoginForm(forms.Form):
    mobile_number = forms.CharField(max_length=15)

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)
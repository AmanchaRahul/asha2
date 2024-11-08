from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SkinCareCheck

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email  
    
    

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



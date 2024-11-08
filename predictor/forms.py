from django import forms

class DiabetesForm(forms.Form):
    Age = forms.IntegerField(
        label='Age',
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter age (0-120)'
        })
    )
    BMI = forms.FloatField(
        label='Body Mass Index (BMI)',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Weight(kg) / (Height(m))²'
        })
    )
    Glucose = forms.FloatField(
        label='Fasting Blood Sugar Level',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter value in mg/dL'
        })
    )
    BloodPressure = forms.FloatField(
        label='Blood Pressure',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter value in mm Hg'
        })
    )


from django import forms

class DiabetesForm(forms.Form):
    Pregnancies = forms.FloatField(label='Number of Pregnancies')
    Glucose = forms.FloatField(label='Glucose level')
    BloodPressure = forms.FloatField(label='Blood Pressure (mm Hg)')
    SkinThickness = forms.FloatField(label='Skin Thickness (mm)')
    Insulin = forms.FloatField(label='Insulin level (mu U/ml)')
    BMI = forms.FloatField(label='Body Mass Index (BMI)')
    DiabetesPedigreeFunction = forms.FloatField(label='Diabetes Pedigree Function')
    Age = forms.FloatField(label='Age')

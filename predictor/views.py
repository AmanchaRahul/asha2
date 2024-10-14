import pickle
import numpy as np
from django.shortcuts import render
from .forms import DiabetesForm

# Load the trained SVM model and scaler
with open('best_svm_model.pkl', 'rb') as model_file:
    svm_model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

def predict_diabetes(request):
    if request.method == 'POST':
        form = DiabetesForm(request.POST)
        if form.is_valid():
            # Get data from the form
            user_data = np.array([[form.cleaned_data['Pregnancies'],
                                   form.cleaned_data['Glucose'],
                                   form.cleaned_data['BloodPressure'],
                                   form.cleaned_data['SkinThickness'],
                                   form.cleaned_data['Insulin'],
                                   form.cleaned_data['BMI'],
                                   form.cleaned_data['DiabetesPedigreeFunction'],
                                   form.cleaned_data['Age']]])
            
            # Preprocess the input
            user_data_scaled = scaler.transform(user_data)
            
            # Predict
            prediction = svm_model.predict(user_data_scaled)
            
            # Prepare the result
            result = "The person is likely to have diabetes." if prediction[0] == 1 else "The person is not likely to have diabetes."
            
            return render(request, 'predictor/result.html', {'result': result})
    else:
        form = DiabetesForm()

    return render(request, 'predictor/predict.html', {'form': form})

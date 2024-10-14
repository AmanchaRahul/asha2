from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_diabetes, name='predict_diabetes'),
]

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ContactForm
from django.contrib import messages
from .models import BloodPressureCheck, DiabetesCheck, SkinCareCheck, UserProfile, DiabetesChallenge, DiabetesChallengeImage, BloodpressureChallenge, BloodpressureChallengeImage, WaterIntake
from datetime import date
from django.views import View
from .services.news_service import get_news
from django.core.mail import send_mail
from django.conf import settings
from .forms import SkinCareCheckForm
from .recommendations import get_skincare_recommendations, get_diet_recommendations
import requests
import random
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from groq import Groq
import os
from django.views.decorators.http import require_http_methods
import json


# Create your views here.
def base_view(request):
    return render(request,"base.html")


def wellness_view(request):
    return render(request,"wellness.html")


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Explicitly specify the backend for username/password login
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f"Welcome back, {username}!")
                return redirect('/wellness/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
   

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicitly specify the backend for signup
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome to ASHA Health, {user.username}!")
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    
    
def logout_view(request):
    logout(request)
    return redirect('/')

def about_view(request):
    return render(request, "about.html")


def diabetes_diet_view(request):
    return render(request,"diabetes/diabetes_diet.html")


def prediabetes_breakfast_view(request):
    return render(request,'diabetes/prediabetes_breakfast.html')


def prediabetes_lunch_view(request):
    return render(request,'diabetes/prediabetes_lunch.html')

def prediabetes_dinner_view(request):
    return render(request,'diabetes/prediabetes_dinner.html')



def type1_breakfast_view(request):
    return render(request,'diabetes/type1_breakfast.html')


def type1_lunch_view(request):
    return render(request,'diabetes/type1_lunch.html')

def type1_dinner_view(request):
    return render(request,'diabetes/type1_dinner.html')



def type2_breakfast_view(request):
    return render(request,'diabetes/type2_breakfast.html')


def type2_lunch_view(request):
    return render(request,'diabetes/type2_lunch.html')

def type2_dinner_view(request):
    return render(request,'diabetes/type2_dinner.html')



def bloodpressure_diet_view(request):
    return render(request,"bloodpressure/bloodpressure_diet.html")



def prehypertension_breakfast_view(request):
    return render(request,'bloodpressure/prehypertension_breakfast.html')


def prehypertension_lunch_view(request):
    return render(request,'bloodpressure/prehypertension_lunch.html')

def prehypertension_dinner_view(request):
    return render(request,'bloodpressure/prehypertension_dinner.html')


def stage1_breakfast_view(request):
    return render(request,'bloodpressure/stage1_breakfast.html')

def stage1_lunch_view(request):
    return render(request,'bloodpressure/stage1_lunch.html')

def stage1_dinner_view(request):
    return render(request,'bloodpressure/stage1_dinner.html')



def stage2_breakfast_view(request):
    return render(request,'bloodpressure/stage2_breakfast.html')


def stage2_lunch_view(request):
    return render(request,'bloodpressure/stage2_lunch.html')

def stage2_dinner_view(request):
    return render(request,'bloodpressure/stage2_dinner.html')


def skincare_diet_view(request):
    return render(request,'skincare/skincare_diet.html')


def diabetes_exercises_view(request):
    return render(request,"diabetes/diabetes_exercises.html")


def bloodpressure_exercises_view(request):
    return render(request,"bloodpressure/bloodpressure_exercises.html")



class BloodPressureCheckView(View):
    def get(self, request):
        return render(request, 'bloodpressure/bloodpressure_check.html')

    def post(self, request):
        systolic = int(request.POST.get('systolic', 0))
        diastolic = int(request.POST.get('diastolic', 0))
        result = self.interpret_blood_pressure(systolic, diastolic)
        BloodPressureCheck.objects.create(systolic=systolic, diastolic=diastolic, result=result)
        return render(request, 'bloodpressure/bloodpressure_check.html', {'result': result})

    def interpret_blood_pressure(self, systolic, diastolic):
        if systolic < 90 or diastolic < 60:
            return 'Low blood pressure'
        elif systolic < 120 and diastolic < 80:
            return 'Normal blood pressure'
        elif 120 <= systolic <= 129 and diastolic < 80:
            return 'Elevated blood pressure'
        elif 130 <= systolic <= 139 or 80 <= diastolic <= 89:
            return 'High blood pressure (Hypertension stage 1)'
        elif systolic >= 140 or diastolic >= 90:
            return 'High blood pressure (Hypertension stage 2)'
        else:
            return 'Hypertensive crisis'
        
    
class DiabetesCheckView(View):
    def get(self, request):
        return render(request, 'diabetes/diabetes_check.html')

    def post(self, request):
        glucose_level = float(request.POST.get('glucose_level', 0))
        result = self.interpret_glucose_level(glucose_level)
        DiabetesCheck.objects.create(glucose_level=glucose_level, result=result)
        return render(request, 'diabetes/diabetes_check.html', {'result': result})

    def interpret_glucose_level(self, level):
        if level < 70:
            return 'Low blood sugar (hypoglycemia)'
        elif 70 <= level <= 99:
            return 'Normal fasting glucose level'
        elif 100 <= level <= 125:
            return 'Prediabetes'
        elif 126 <= level <= 199:
            return 'Elevated glucose - possible Type 1 or Type 2 Diabetes (Further testing required)'
        elif level >= 200:
            return 'High glucose - possible Type 1 or Type 2 Diabetes (Immediate medical attention recommended)'
        else:
            return 'Invalid glucose level'
        


  # Make sure this import is correct
def health_news(request):
    diabetes_news = get_news('diabetes')  # More specific query
    blood_pressure_news = get_news('blood pressure OR hypertension OR high blood pressure OR low blood pressure')
    skincare_news = get_news('skincare')
    
    
    print(f"Diabetes news count: {len(diabetes_news)}")
    print(f"Blood pressure news count: {len(blood_pressure_news)}")
    print(f"Skincare news count: {len(skincare_news)}")

    context = {
        'diabetes_news': diabetes_news,
        'blood_pressure_news': blood_pressure_news,
        'skincare_news': skincare_news
    }
    
    return render(request, 'news.html', context)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            frommail = form.cleaned_data['email']
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            
            # Send email
            subject = f"New contact form submission: {topic}"
            email_message = f"Name: {name}\nEmail: {frommail}\nTopic: {topic}\n\nMessage:\n{message}"
            
            send_mail(subject, email_message, frommail, ['amancharahul25@gmail.com',frommail] )
            # Redirect to a thank you page or show a success message
            return redirect('/thankyou/')  # You'll need to create this view and template
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})



def thankyou_view(request):
    return render(request,"thankyou.html")



def skincare_routine_view(request):
    return render(request,"skincare/skincare_routine.html")
        




class SkinCareCheckView(View):
    def get(self, request):
        form = SkinCareCheckForm()
        return render(request, 'skincare/skincare_check.html', {'form': form})

    def post(self, request):
        form = SkinCareCheckForm(request.POST)
        if form.is_valid():
            skin_type = form.cleaned_data['skin_type']
            concerns = form.cleaned_data['concerns']
            
            skincare_recommendations = get_skincare_recommendations(skin_type, concerns)
            diet_recommendations = get_diet_recommendations(skin_type, concerns)
            
            context = {
                'skin_type': skin_type,
                'concerns': concerns,
                'skincare_recommendations': skincare_recommendations,
                'diet_recommendations': diet_recommendations,
            }
            return render(request, 'skincare/skincare_recommendations.html', context)
        return render(request, 'skincare/skincare_check.html', {'form': form})
    
    


def manage_stress(request):
    stress_techniques = [
        {
            "name": "Deep Breathing",
            "description": "Practice deep, slow breathing for 5-10 minutes daily to reduce stress and lower blood pressure."
        },
        {
            "name": "Progressive Muscle Relaxation",
            "description": "Tense and then relax each muscle group in your body to release physical tension and mental stress."
        },
        {
            "name": "Mindfulness Meditation",
            "description": "Focus on the present moment to reduce anxiety about the future and regrets about the past."
        },
        {
            "name": "Regular Exercise",
            "description": "Engage in moderate exercise for 30 minutes a day to reduce stress and lower blood pressure."
        }
    ]
    return render(request, 'bloodpressure/manage_stress.html', {'stress_techniques': stress_techniques})


def anti_aging_tips(request):
    anti_aging_tips = [
        {
            "name": "Sun Protection",
            "description": "Use broad-spectrum sunscreen daily and wear protective clothing to prevent premature aging from UV rays."
        },
        {
            "name": "Hydration",
            "description": "Drink plenty of water and use a good moisturizer to keep your skin hydrated and plump."
        },
        {
            "name": "Antioxidant-Rich Diet",
            "description": "Consume foods high in antioxidants like berries, leafy greens, and nuts to fight free radical damage."
        },
        {
            "name": "Retinoids",
            "description": "Use retinoid creams to boost collagen production and reduce fine lines and wrinkles."
        }
    ]
    return render(request, 'skincare/anti_aging_tips.html', {'anti_aging_tips': anti_aging_tips})




def manage_diabetes_medication(request):
    diabetes_medications = [
        {
            "name": "Metformin",
            "description": "A first-line medication that reduces glucose production in the liver and improves insulin sensitivity.",
            "side_effects": "Nausea, diarrhea, stomach upset (usually temporary)."
        },
        {
            "name": "Sulfonylureas",
            "description": "Stimulate the pancreas to produce more insulin. Examples include glipizide and glyburide.",
            "side_effects": "Hypoglycemia, weight gain."
        },
        {
            "name": "DPP-4 Inhibitors",
            "description": "Help the body continue to make insulin. Examples include sitagliptin and linagliptin.",
            "side_effects": "Upper respiratory tract infection, headache, inflammation of the pancreas (rare)."
        },
        {
            "name": "GLP-1 Receptor Agonists",
            "description": "Slow digestion and help lower blood glucose levels. Examples include liraglutide and semaglutide.",
            "side_effects": "Nausea, vomiting, diarrhea (usually improves over time)."
        },
        {
            "name": "SGLT2 Inhibitors",
            "description": "Help the kidneys remove glucose from the body through urine. Examples include empagliflozin and dapagliflozin.",
            "side_effects": "Urinary tract infections, genital yeast infections, dehydration."
        }
    ]

    medication_tips = [
        {
            "title": "Stick to Your Schedule",
            "description": "Take your medications at the same time each day to maintain consistent blood sugar levels."
        },
        {
            "title": "Use a Pill Organizer",
            "description": "A weekly pill organizer can help you keep track of your medications and ensure you don't miss a dose."
        },
        {
            "title": "Set Reminders",
            "description": "Use your phone or a smart device to set alarms reminding you when it's time to take your medication."
        },
        {
            "title": "Understand Your Medications",
            "description": "Learn about each medication you're taking, including its purpose, proper dosage, and potential side effects."
        },
        {
            "title": "Monitor and Record",
            "description": "Keep a log of your blood sugar levels, medication doses, and any side effects you experience."
        },
        {
            "title": "Be Prepared for Travel",
            "description": "When traveling, pack extra medication and supplies. Carry a doctor's note and prescriptions for all your medications."
        },
        {
            "title": "Communicate with Your Healthcare Team",
            "description": "Regularly discuss your medication regimen with your doctor, especially if you're experiencing side effects or your blood sugar levels are not well-controlled."
        }
    ]

    context = {
        'diabetes_medications': diabetes_medications,
        'medication_tips': medication_tips
    }

    return render(request, 'diabetes/manage_diabetes_medication.html', context)



def diabetes_challenge(request):
    return render(request,"diabetes/diabetes_selection_challenge.html")

def bloodpressure_challenge(request):
    return render(request,"bloodpressure/bloodpressure_selection_challenge.html")

#====================================================================================

@login_required
def thirty_day_challenge(request):
    challenge, created = DiabetesChallenge.objects.get_or_create(
        user=request.user,
        duration=30,
        defaults={'start_date': timezone.now().date()}
    )
    days = range(1, 31)
    images = DiabetesChallengeImage.objects.filter(challenge=challenge)
    image_dict = {image.day: image.get_image_url() for image in images}
    return render(request, 'diabetes/30_day_challenge.html', {'days': days, 'images': image_dict})

@login_required
def sixty_day_challenge(request):
    challenge, created = DiabetesChallenge.objects.get_or_create(
        user=request.user,
        duration=60,
        defaults={'start_date': timezone.now().date()}
    )
    days = range(1, 61)
    images = DiabetesChallengeImage.objects.filter(challenge=challenge)
    image_dict = {image.day: image.get_image_url() for image in images}
    return render(request, 'diabetes/60_day_challenge.html', {'days': days, 'images': image_dict})

@login_required
def ninety_day_challenge(request):
    challenge, created = DiabetesChallenge.objects.get_or_create(
        user=request.user,
        duration=90,
        defaults={'start_date': timezone.now().date()}
    )
    days = range(1, 91)
    images = DiabetesChallengeImage.objects.filter(challenge=challenge)
    image_dict = {image.day: image.get_image_url() for image in images}
    return render(request, 'diabetes/90_day_challenge.html', {'days': days, 'images': image_dict})



@login_required
def upload_image(request, duration, day):
    if request.method == 'POST' and request.FILES.get('image'):
        challenge = get_object_or_404(DiabetesChallenge, user=request.user, duration=duration)
        image = request.FILES['image']
        DiabetesChallengeImage.objects.update_or_create(
            challenge=challenge, day=day,
            defaults={'image': image}
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_image(request, duration, day):
    if request.method == 'POST':
        challenge = get_object_or_404(DiabetesChallenge, user=request.user, duration=duration)
        DiabetesChallengeImage.objects.filter(challenge=challenge, day=day).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
#===================================================================================


@login_required
def b_thirty_day_challenge(request):
    challenge, created = BloodpressureChallenge.objects.get_or_create(
        user=request.user,
        duration=30,
        defaults={'start_date': timezone.now().date()}
    )
    days = range(1, 31)
    bloodpressure_images = BloodpressureChallengeImage.objects.filter(challenge=challenge)
    image_dict = {image.day: image.get_image_url() for image in bloodpressure_images}
    return render(request, 'bloodpressure/30_day_challenge.html', {'days': days, 'bloodpressure_images': image_dict})


@login_required
def b_sixty_day_challenge(request):
    challenge, created = BloodpressureChallenge.objects.get_or_create(
        user=request.user,
        duration=60,
        defaults={'start_date': timezone.now().date()}
    )
    days = range(1, 61)
    bloodpressure_images = BloodpressureChallengeImage.objects.filter(challenge=challenge)
    image_dict = {image.day: image.get_image_url() for image in bloodpressure_images}
    return render(request, 'bloodpressure/60_day_challenge.html', {'days': days, 'bloodpressure_images': image_dict})


@login_required
def b_ninety_day_challenge(request):
    challenge, created = BloodpressureChallenge.objects.get_or_create(
        user=request.user,
        duration=90,
        defaults={'start_date': timezone.now().date()}
    )
    days = range(1, 91)
    bloodpressure_images = BloodpressureChallengeImage.objects.filter(challenge=challenge)
    image_dict = {image.day: image.get_image_url() for image in bloodpressure_images}
    return render(request, 'bloodpressure/90_day_challenge.html', {'days': days, 'bloodpressure_images': image_dict})




@login_required
def upload_bloodpressure_image(request, duration, day):
    if request.method == 'POST' and request.FILES.get('image'):
        # Get the BloodpressureChallenge for the current user and duration
        challenge = get_object_or_404(BloodpressureChallenge, user=request.user, duration=duration)
        image = request.FILES['image']
        # Update or create the image for the given day and challenge
        BloodpressureChallengeImage.objects.update_or_create(
            challenge=challenge, day=day,
            defaults={'image': image}
        )
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def delete_bloodpressure_image(request, duration, day):
    if request.method == 'POST':
        # Get the BloodpressureChallenge for the current user and duration
        challenge = get_object_or_404(BloodpressureChallenge, user=request.user, duration=duration)
        # Delete the image for the given day and challenge
        BloodpressureChallengeImage.objects.filter(challenge=challenge, day=day).delete()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'}, status=400)

#====================================================================================


@login_required
def first_last_day_diabetes_images(request, duration):
    # Get the challenge
    challenge = get_object_or_404(DiabetesChallenge, user=request.user, duration=duration)
    
    # Get the first and last day images (first day is day 1, last day is based on duration)
    first_image = DiabetesChallengeImage.objects.filter(challenge=challenge, day=1).first()
    last_image = DiabetesChallengeImage.objects.filter(challenge=challenge, day=duration).first()
    
    return render(request, 'diabetes/first_last_images.html', {
        'first_image': first_image,
        'last_image': last_image,
        'duration': duration
    })

@login_required
def first_last_day_bloodpressure_images(request, duration):
    # Get the challenge
    challenge = get_object_or_404(BloodpressureChallenge, user=request.user, duration=duration)
    
    # Get the first and last day images (first day is day 1, last day is based on duration)
    first_image = BloodpressureChallengeImage.objects.filter(challenge=challenge, day=1).first()
    last_image = BloodpressureChallengeImage.objects.filter(challenge=challenge, day=duration).first()
    
    return render(request, 'bloodpressure/first_last_images.html', {
        'first_image': first_image,
        'last_image': last_image,
        'duration': duration
    })



#====================================================================================
import logging



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Make sure to import your client correctly

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an AI assistant for a Asha wellness webapp that focuses on providing information about diabetes, blood pressure, and skincare. Your responses should be limited to these topics and general information about the company and its services. Do not provide any information outside of these areas. Be concise, accurate, and helpful.

Key points:
1. Only discuss diabetes, blood pressure, and skincare.
2. Provide information about the company's wellness services related to these topics.
3. Do not offer medical advice or diagnoses.
4. If asked about topics outside your scope, politely redirect to the main topics.
5. Keep responses brief and to the point.
"""

@csrf_exempt
@require_http_methods(["GET", "POST"])
def chatbot(request):
    logger.info(f"Request method: {request.method}")

    if request.method == 'POST':
        logger.info("Received POST request")

        try:
            data = json.loads(request.body)
            user_input = data.get('user_input')
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from request body")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        logger.info(f"User input: {user_input}")

        if user_input:
            try:
                chat_completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=512,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                
                response = chat_completion.choices[0].message.content
                logger.info(f"Bot response: {response}")

                return JsonResponse({'user_input': user_input, 'response': response})
            except Exception as e:
                logger.error(f"Error calling Groq API: {str(e)}")
                return JsonResponse({'error': 'Failed to get response from chatbot'}, status=500)
        else:
            return JsonResponse({'error': 'No user input provided'}, status=400)

    return render(request, 'chat.html')



@csrf_exempt
def voice_view(request):
    if request.method == 'POST':
        user_text = request.POST.get('user_text', '').lower()

        if not user_text:
            return JsonResponse({'error': 'No input provided'}, status=400)

        # Check for stop command
        if 'stop' in user_text:
            return JsonResponse({
                'status': 'Speech stopped',
                'llama_response': 'Voice command recognized: Stopping.',
                'should_stop': True
            })

        try:
            # Get LLaMA response with SYSTEM_PROMPT
            chat_completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.7,
                max_tokens=512,
                top_p=1,
                stream=False,
                stop=None,
            )
            llama_response = chat_completion.choices[0].message.content
            logger.info(f"LLaMA response: {llama_response}")

            return JsonResponse({
                'llama_response': llama_response,
                'should_stop': False
            })
        except Exception as e:
            logger.error(f"Error in voice_view: {str(e)}")
            return JsonResponse({'error': 'Failed to get response from chatbot'}, status=500)

    return render(request, 'voice.html')




    
@login_required
def water_intake_tracker(request):
    # Get the current user's water intake data
    water_intake, created = WaterIntake.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        water_intake.total_liters += amount
        water_intake.save()

        # Check if the user has met the goal
        if water_intake.total_liters >= 5.0:  # Check if total liters are 5 or more
            messages.success(request, "Congratulations! You have completed your goal of drinking 5 liters of water!")  # Success message

    total_liters = water_intake.total_liters
    goal_liters = 5.0  # Set your goal to 5 liters

    context = {
        'total_liters': total_liters,
        'goal_liters': goal_liters,
    }
    return render(request, 'skincare/water_tracker.html', context)   





@login_required
def reset_water_intake(request):
    # Reset the user's water intake
    water_intake, created = WaterIntake.objects.get_or_create(user=request.user)
    water_intake.total_liters = 0.0  # Reset to 0
    water_intake.save()

    return redirect('water_intake_tracker') 
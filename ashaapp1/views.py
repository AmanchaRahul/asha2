from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ContactForm
from django.contrib import messages
from .models import BloodPressureCheck, DiabetesCheck, SkinCareCheck, UserProfile, DiabetesChallenge, DiabetesChallengeImage, BloodpressureChallenge, BloodpressureChallengeImage, WaterIntake, DailyCheckIn
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
from django.templatetags.static import static
from django.views.decorators.http import require_POST







# Create your views here.
def base_view(request):
    return render(request,"base.html")



@login_required
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
   
   
# views.py

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()
            
            # Create UserProfile (assuming you have this model)
            UserProfile.objects.create(user=user, full_name=form.cleaned_data.get('full_name'))
            
            # Email activation setup
            domain = 'asha2.onrender.com' 
            mail_subject = 'Activate your account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            
            # Sending the email using send_mail
            send_mail(
                subject=mail_subject,
                message=message,
                from_email='amancharahul25@gmail.com',  # Change to your "from" email address
                recipient_list=[to_email],
                fail_silently=False,
            )

            return render(request, 'account_activation_sent.html')  # Redirect to success page
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

# views.py
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.models import User

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_verified = True
        user.save()
        user.userprofile.save()
        # Log in the user, specifying the backend
        backend = 'django.contrib.auth.backends.ModelBackend'  # Or your custom backend if you have one
        login(request, user, backend=backend)
        return redirect('/wellness/')
      
    else:
        return render(request, 'account_activation_invalid.html')

    
    
    
def logout_view(request):
    logout(request)
    return redirect('/')

def about_view(request):
    return render(request, "about.html")



@login_required
def diabetes_diet_view(request):
    return render(request,"diabetes/diabetes_diet.html")




@login_required
def bloodpressure_diet_view(request):
    return render(request,"bloodpressure/bloodpressure_diet.html")


@login_required
def skincare_diet_view(request):
    # Get or create a DailyCheckIn record for the current user
    daily_check_in, created = DailyCheckIn.objects.get_or_create(user=request.user)
    
    context = {
        'check_in_count': daily_check_in.check_in_count
    }
    return render(request, 'skincare/skincare_diet.html', context)


@login_required
@require_POST
def daily_checkin(request):
    daily_check_in, created = DailyCheckIn.objects.get_or_create(user=request.user)
    daily_check_in.check_in_count += 1
    daily_check_in.save()
    return JsonResponse({
        'success': True, 
        'check_in_count': daily_check_in.check_in_count
    })

@login_required
@require_POST
def reset_checkin(request):
    daily_check_in, created = DailyCheckIn.objects.get_or_create(user=request.user)
    daily_check_in.reset_count()
    return JsonResponse({
        'success': True, 
        'check_in_count': 0
    })


from django.db.models import Avg, Sum
from datetime import datetime, timedelta
from .models import ExerciseLog, WeeklyStats, BloodPressureExerciseLog
from .forms import ExerciseLogForm, BloodPressureExerciseLogForm
from django.db.models import Avg, Q  


    
@login_required
def diabetes_exercises_view(request):
    if request.method == 'POST':
        form = ExerciseLogForm(request.POST)
        if form.is_valid():
            exercise_log = form.save(commit=False)
            exercise_log.user = request.user
            exercise_log.save()
            return redirect('diabetesexercises')
    else:
        form = ExerciseLogForm()

    # Get user's exercise logs for the past week
    week_ago = datetime.now() - timedelta(days=7)
    exercise_logs = ExerciseLog.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by('-date')
    
    
    latest_exercise_logs = exercise_logs[:5]

    # Calculate weekly stats
    weekly_stats = {
        'exercise_minutes': exercise_logs.aggregate(total=Sum('duration'))['total'] or 0,
        'glucose_stability': calculate_glucose_stability(exercise_logs),
        'active_days': exercise_logs.values('date').distinct().count(), 
        'energy_level': calculate_energy_level(exercise_logs)
    }


    # Get glucose data for the chart
    glucose_data = get_glucose_chart_data(exercise_logs)

    context = {
        'form': form,
        'exercise_logs': latest_exercise_logs,
        'weekly_stats': weekly_stats,
        'glucose_data': glucose_data,
    }
    return render(request,"diabetes/diabetes_exercises.html",context)


def calculate_glucose_stability(logs):
    if not logs:
        return 0
    
    total_readings = logs.count() * 2  # before and after readings
    in_range_readings = logs.filter(
        Q(blood_sugar_before__range=(70, 180)) |  # Use Q directly instead of models.Q
        Q(blood_sugar_after__range=(70, 180))
    ).count()
    
    return (in_range_readings / total_readings) * 100 if total_readings > 0 else 0

def calculate_energy_level(logs):
    if not logs:
        return 0  # Return 0 if no exercise logs are available

    # Calculate average exercise duration (in minutes)
    avg_duration = logs.aggregate(avg=Avg('duration'))['avg'] or 0

    # Calculate the number of active days in the last 7 days
    active_days = logs.dates('date', 'day').count()
    
    # Consistency factor: reward more days of activity in the week
    consistency_factor = active_days / 7  # The more active days, the higher this factor

    # Calculate energy level (considering duration and consistency factor)
    energy_level = (avg_duration / 30) * 10 * consistency_factor

    # Cap energy level at 10
    return min(energy_level, 10)




def get_glucose_chart_data(logs):
    if not logs:
        return json.dumps({
            'dates': [],
            'before_values': [],
            'after_values': []
        })
    
    days_of_week = [] 
    before_values = []
    after_values = []
    
    for log in logs:
        day_of_week = log.date.strftime('%A') 
        days_of_week.append(day_of_week)
        before_values.append(float(log.blood_sugar_before))
        after_values.append(float(log.blood_sugar_after))
    
    # Add debug print
    data = {
        'dates': days_of_week,  
        'before_values': before_values,
        'after_values': after_values
    }
    print("Glucose Data:", data)  # Debug print
    return json.dumps(data)


@login_required
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
            
            send_mail(subject, email_message, settings.EMAIL_HOST_USER, ['amancharahul25@gmail.com',frommail] )
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


@login_required
def diabetes_challenge(request):
    return render(request,"diabetes/diabetes_selection_challenge.html")

@login_required
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
            
            if not user_input:
                return JsonResponse({'error': 'No user input provided'}, status=400)

            logger.info(f"Processing user input: {user_input}")

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

            return JsonResponse({
                'response': response
            })

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

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



@login_required
def bloodpressure_exercises_view(request):
    if request.method == 'POST':
        form = BloodPressureExerciseLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('bloodpressureexercises')
    else:
        form = BloodPressureExerciseLogForm()

    # Get all logs for the user
    all_logs = BloodPressureExerciseLog.objects.filter(user=request.user).order_by('-date')

    # Prepare context variables with default values
    exercise_minutes = 0
    bp_stability = 0
    energy_level = 0

    # Calculate daily statistics if logs exist
    if all_logs.exists():
        # Get the most recent log's date
        latest_date = all_logs.first().date.date()
        
        # Filter logs for the most recent date
        latest_day_logs = all_logs.filter(date__date=latest_date)
        
        # Calculate statistics for the latest day
        exercise_minutes = latest_day_logs.aggregate(total_minutes=Sum('duration'))['total_minutes'] or 0
        bp_stability = calculate_bp_stability(latest_day_logs)
        energy_level = latest_day_logs.aggregate(avg_energy=Avg('energy_boost'))['avg_energy'] or 0

    # Prepare data for the graph
    bp_data = prepare_bp_graph_data_daily(all_logs)
    
    # Count active days
    active_days = all_logs.values('date').distinct().count()

    context = {
        'form': form,
        'exercise_logs': all_logs[:5],  # Show the latest 5 logs
        'exercise_minutes': exercise_minutes,
        'bp_stability': bp_stability,
        'energy_level': energy_level,
        'bp_data': json.dumps(bp_data),
        'active_days': active_days,
    }

    return render(request, 'bloodpressure/bloodpressure_exercises.html', context)


def calculate_daily_stats(logs):
    """Calculate daily statistics for exercise logs."""
    daily_stats = {}
    # Get unique dates and aggregate data for each day
    unique_dates = logs.values_list('date__date', flat=True).distinct()

    for date in unique_dates:
        day_logs = logs.filter(date__date=date)

        daily_stats[date.strftime('%A')] = {
            'exercise_minutes': day_logs.aggregate(total_minutes=Sum('duration'))['total_minutes'] or 0,
            'energy_level': day_logs.aggregate(avg_energy=Avg('energy_boost'))['avg_energy'] or 0,
            'bp_stability': calculate_bp_stability(day_logs),
        }

    return daily_stats


def calculate_bp_stability(logs):
    """Calculate blood pressure stability percentage based on exercise logs."""
    if not logs:
        return 0

    positive_indicators = logs.filter(
        feeling_after_exercise__in=['great', 'normal']
    ).count()

    total_logs = logs.count()
    return (positive_indicators / total_logs * 100) if total_logs > 0 else 0


def prepare_bp_graph_data_daily(logs):
    """Prepare data for the blood pressure trends graph with daily data."""
    days = []
    feeling_great = []
    feeling_normal = []

    # Get all unique dates
    unique_dates = logs.values_list('date__date', flat=True).distinct()

    for date in unique_dates:
        day_logs = logs.filter(date__date=date)

        # Append day name
        days.append(date.strftime('%A'))

        # Calculate percentages for 'great' and 'normal' feelings
        great_count = day_logs.filter(feeling_after_exercise='great').count()
        great_percentage = (great_count / day_logs.count() * 100) if day_logs.count() > 0 else 0
        feeling_great.append(great_percentage)

        normal_count = day_logs.filter(feeling_after_exercise='normal').count()
        normal_percentage = (normal_count / day_logs.count() * 100) if day_logs.count() > 0 else 0
        feeling_normal.append(normal_percentage)

    return {
        'days': days,
        'feeling_great': feeling_great,
        'feeling_normal': feeling_normal,
    }





def ddoctor_view(request):
    return render(request, 'diabetes/ddoctor.html')


def bdoctor_view(request):
    return render(request, 'bloodpressure/bdoctor.html')

def sdoctor_view(request):
    return render(request, 'skincare/sdoctor.html')


def heart_model(request):
    # Pass the heart.glb file to the template
    model_url = static('images/human_heart.glb')
    info_content = {
        'title': 'Diabetes and Heart Health',
        'description': 'Diabetes can significantly impact heart health by damaging blood vessels and nerves. Prolonged high blood sugar levels can lead to:',
        'key_points': [
            'Increased risk of cardiovascular disease',
            'Higher chances of heart attacks and strokes',
            'Potential damage to heart muscle and blood vessels',
            'Elevated risk of heart failure',
            'Importance of managing blood sugar and maintaining a healthy lifestyle'
        ]
    }
    return render(request, 'heart_blood.html', {
        'model_url': model_url, 
        'info_content': info_content,
        'model_type': 'heart'
    })

def blood_pressure_model(request):
    # Pass the bloodpressure.glb file to the template
    model_url = static('images/cell.glb')
    info_content = {
        'title': 'Blood Cells and Pressure Dynamics',
        'description': 'Blood cells play a crucial role in maintaining healthy blood pressure and overall cardiovascular function:',
        'key_points': [
            'Red blood cells transport oxygen throughout the body',
            'Healthy blood flow is essential for maintaining optimal blood pressure',
            'Blood cell count and quality impact cardiovascular health',
            'Factors like hydration, exercise, and diet influence blood cell performance',
            'Regular monitoring of blood cell parameters is important for health'
        ]
    }
    return render(request, 'heart_blood.html', {
        'model_url': model_url, 
        'info_content': info_content,
        'model_type': 'blood_cell'
    })
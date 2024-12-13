
from django.urls import path
from ashaapp1 import views
from .views import BloodPressureCheckView, DiabetesCheckView, health_news, SkinCareCheckView



urlpatterns = [

    path('',views.base_view,name="basedata"),
    path('wellness/',views.wellness_view,name="wellnessdata"),
    path('login/',views.login_view,name="logindata"),
    path('signup/',views.signup_view,name="signupdata"),
    path('logout/',views.logout_view,name="logoutdata"),
    path('about/',views.about_view,name="aboutdata"),
    
    
    path('diabetes_diet/',views.diabetes_diet_view,name="diabetesdietdata"),
    
    
    
    path('bloodpressure_diet/',views.bloodpressure_diet_view,name="bloodpressuredietdata"),
   
    
   
    path('skincare_diet/', views.skincare_diet_view, name='skincaredietdata'),
    path('daily-checkin/', views.daily_checkin, name='daily_checkin'),
    path('reset-checkin/', views.reset_checkin, name='reset_checkin'),
    
    
    path('diabetesexercises/',views.diabetes_exercises_view,name="diabetesexercises"),
    
    path('bloodpressureexercises/',views.bloodpressure_exercises_view,name="bloodpressureexercises"),
    
    
    path('bloodpressurecheck/', BloodPressureCheckView.as_view(), name='blood_pressure_check'),
    
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 


    path('diabetescheck/', DiabetesCheckView.as_view(), name='diabetes_check'),
    
   
    path('news/', health_news, name='newsdata'),
    
    path('contact/', views.contact_view,name="contactdata"),
    
    path('thankyou/', views.thankyou_view,name="thankyoudata"),
    
    path('skincareroutine/', views.skincare_routine_view,name="skincareroutine"),
    
    path('skincare-check/', SkinCareCheckView.as_view(), name='skincarecheckdata'),
    
    path('manage-stress/', views.manage_stress, name='manage_stress'),
    path('anti-aging-tips/', views.anti_aging_tips, name='anti_aging_tips'),
    path('manage-diabetes-medications/', views.manage_diabetes_medication, name='manage_diabetes_medications'),
    path('water-intake/', views.water_intake_tracker, name='water_intake_tracker'),
    path('reset-water-intake/', views.reset_water_intake, name='reset_water_intake'),  # Add this line


    path('diabeteschallenge/',views.diabetes_challenge,name='diabeteschallenge'),
    path('bloodpressurechallenge/',views.bloodpressure_challenge,name='bloodpressurechallenge'),
    
    path('diabetes30/', views.thirty_day_challenge, name='thirty_day_challenge'),
    path('diabetes60/', views.sixty_day_challenge, name='sixty_day_challenge'),
    path('diabetes90/', views.ninety_day_challenge, name='ninety_day_challenge'),
    path('diabetes30/upload/<int:day>/', views.upload_image, {'duration': 30}, name='upload_image_30'),
    path('diabetes60/upload/<int:day>/', views.upload_image, {'duration': 60}, name='upload_image_60'),
    path('diabetes90/upload/<int:day>/', views.upload_image, {'duration': 90}, name='upload_image_90'),
    path('diabetes30/delete/<int:day>/', views.delete_image, {'duration': 30}, name='delete_image_30'),
    path('diabetes60/delete/<int:day>/', views.delete_image, {'duration': 60}, name='delete_image_60'),
    path('diabetes90/delete/<int:day>/', views.delete_image, {'duration': 90}, name='delete_image_90'),
    
    
    
    path('bloodpressure30/', views.b_thirty_day_challenge, name='b_thirty_day_challenge'),
    path('bloodpressure60/', views.b_sixty_day_challenge, name='b_sixty_day_challenge'),
    path('bloodpressure90/', views.b_ninety_day_challenge, name='b_ninety_day_challenge'),
    path('bloodpressure30/upload/<int:day>/', views.upload_bloodpressure_image, {'duration': 30}, name='b_upload_image_30'),
    path('bloodpressure30/delete/<int:day>/', views.delete_bloodpressure_image, {'duration': 30}, name='b_delete_image_30'),
    path('bloodpressure60/upload/<int:day>/', views.upload_bloodpressure_image, {'duration': 60}, name='b_upload_image_60'),
    path('bloodpressure60/delete/<int:day>/', views.delete_bloodpressure_image, {'duration': 60}, name='b_delete_image_60'),
    path('bloodpressure90/upload/<int:day>/', views.upload_bloodpressure_image, {'duration': 90}, name='b_upload_image_90'),
    path('bloodpressure90/delete/<int:day>/', views.delete_bloodpressure_image, {'duration': 90}, name='b_delete_image_90'),
   
    
    # Diabetes first and last image comparison
    path('diabetes/compare/<int:duration>/', views.first_last_day_diabetes_images, name='diabetes_first_last_images'),

    # Blood pressure first and last image comparison
    path('bloodpressure/compare/<int:duration>/', views.first_last_day_bloodpressure_images, name='bloodpressure_first_last_images'),
       
       
        
    path('chat/', views.chatbot, name='chatbot'), 
    
    
    path('voice/', views.voice_view, name='voice'),
    

    path('ddoctor/', views.ddoctor_view, name="ddoctor"),
    path('bdoctor/', views.bdoctor_view, name="bdoctor"),
    path('sdoctor/', views.sdoctor_view, name="sdoctor"),
    
    
    
    
    
    path('heart/', views.heart_model, name='heart_model'),
    
    path('bloodpressure/', views.blood_pressure_model, name='blood_pressure_model'),
    
    
    path('chat/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
    path('nutritionist_dashboard/', views.nutritionist_dashboard, name='nutritionist_dashboard'),
    path('chat_with_nutritionist/', views.chat_with_nutritionist, name='chat_with_nutritionist'),

    
   
    path('calorie-tracker/', views.calorie_tracker, name='calorie_tracker'),
    path('api/analyze-food/', views.analyze_food, name='analyze_food'),
   
]
    




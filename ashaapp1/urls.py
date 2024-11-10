
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
    path('prediabetesbreakfast/',views.prediabetes_breakfast_view,name="prediabetesbreakfastdata"),
    path('prediabeteslunch/', views.prediabetes_lunch_view, name='prediabeteslunchdata'),
    path('prediabetesdinner/', views.prediabetes_dinner_view, name='prediabetesdinnerdata'),
    path('type1breakfast/', views.type1_breakfast_view, name='type1breakfastdata'),
    path('type1lunch/', views.type1_lunch_view, name='type1lunchdata'),
    path('type1dinner/', views.type1_dinner_view, name='type1dinnerdata'),
    path('type2breakfast/', views.type2_breakfast_view, name='type2breakfastdata'),
    path('type2lunch/', views.type2_lunch_view, name='type2lunchdata'),
    path('type2dinner/', views.type2_dinner_view, name='type2dinnerdata'),
    
    
    path('bloodpressure_diet/',views.bloodpressure_diet_view,name="bloodpressuredietdata"),
    path('prehypertenisonbreakfast/',views.prehypertension_breakfast_view,name="prehypertensionbreakfastdata"),
    path('prehypertensionlunch/', views.prehypertension_lunch_view, name='prehypertensionlunchdata'),
    path('prehypertensiondinner/', views.prehypertension_dinner_view, name='prehypertensiondinnerdata'),
    path('stage1breakfast/', views.stage1_breakfast_view, name='stage1breakfastdata'),
    path('stage1lunch/', views.stage1_lunch_view, name='stage1lunchdata'),
    path('stage1dinner/', views.stage1_dinner_view, name='stage1dinnerdata'),
    path('stage2breakfast/', views.stage2_breakfast_view, name='stage2breakfastdata'),
    path('stage2lunch/', views.stage2_lunch_view, name='stage2lunchdata'),
    path('stage2dinner/', views.stage2_dinner_view, name='stage2dinnerdata'),
    
   
    path('skincare_diet/',views.skincare_diet_view,name="skincaredietdata"),
    
    
    path('diabetesexercises/',views.diabetes_exercises_view,name="diabetesexercises"),
    
    path('bloodpressureexercises/',views.bloodpressure_exercises_view,name="bloodpressureexercises"),
    
    
    path('bloodpressurecheck/', BloodPressureCheckView.as_view(), name='blood_pressure_check'),
    
    
   


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
    
]
    




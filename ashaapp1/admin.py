from django.contrib import admin
from .models import UserProfile, DiabetesCheck, BloodPressureCheck, SkinCareCheck, DiabetesChallenge, DiabetesChallengeImage, BloodpressureChallenge, BloodpressureChallengeImage
from .models import DailyCheckIn
from .models import ExerciseLog, WeeklyStats
from .models import BloodPressureExerciseLog
from .models import UserActivity

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_activity', 'is_online')
    list_filter = ('is_online',)
    search_fields = ('user__username', 'user__email')
    ordering = ('-last_activity',)


@admin.register(BloodPressureExerciseLog)
class BloodPressureExerciseLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_type', 'duration', 'feeling_after_exercise', 'date']
    list_filter = ['exercise_type', 'feeling_after_exercise', 'date']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'date'
    
    
@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise_type', 'duration', 'blood_sugar_before', 'blood_sugar_after', 'date')
    list_filter = ('user', 'exercise_type', 'date')
    search_fields = ('user__username', 'exercise_type', 'notes')
    date_hierarchy = 'date'

@admin.register(WeeklyStats)
class WeeklyStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_start', 'exercise_minutes', 'glucose_stability', 'active_days', 'energy_level')
    list_filter = ('user', 'week_start')
    search_fields = ('user__username',)
    date_hierarchy = 'week_start'
    

# Define a custom admin class for DailyCheckIn
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_in_count', 'reset_count')
    list_filter = ('user',)
    search_fields = ('user__username',)
    actions = ['reset_check_in_count']

    # Custom action to reset the check-in count
    def reset_check_in_count(self, request, queryset):
        for obj in queryset:
            obj.reset_count()
        self.message_user(request, "Selected check-in counts have been reset.")

    reset_check_in_count.short_description = "Reset check-in count to 0"

# Register the model with the custom admin class
admin.site.register(DailyCheckIn, DailyCheckInAdmin)




class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')  # Customize as needed
    

# Customizing the DiabetesCheck admin view
class DiabetesCheckAdmin(admin.ModelAdmin):
    list_display = ('glucose_level', 'result', 'timestamp')  # Display these fields in the admin list
    list_filter = ('timestamp', 'result')  # Add filters for these fields
    search_fields = ('glucose_level', 'result')  # Enable search by glucose_level and result
    ordering = ('-timestamp',)  # Show the most recent check at the top

# Customizing the BloodPressureCheck admin view
class BloodPressureCheckAdmin(admin.ModelAdmin):
    list_display = ('systolic', 'diastolic', 'result', 'timestamp')  # Display systolic, diastolic, result, timestamp
    list_filter = ('timestamp', 'result')  # Filter checks by timestamp and result
    search_fields = ('systolic', 'diastolic', 'result')  # Enable search by blood pressure levels and result
    ordering = ('-timestamp',)  # Order by the most recent check first




class SkinCareCheckAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('skin_type', 'concerns', 'check_date')
    
    # Add filtering options for skin type and check date
    list_filter = ('skin_type', 'check_date')
    
    # Allow searching by skin type and concerns
    search_fields = ('skin_type', 'concerns')
    
    # Order records by date (most recent first)
    ordering = ('-check_date',)
    
    



class DiabetesChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'duration', 'start_date')
    list_filter = ('duration',)
    search_fields = ('user__username',)

class DiabetesChallengeImageAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_duration', 'day', 'uploaded_at')
    list_filter = ('challenge__duration', 'day')
    search_fields = ('challenge__user__username',)
    ordering = ('challenge__user', 'challenge__duration', 'day')

    def get_user(self, obj):
        return obj.challenge.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'challenge__user'

    def get_duration(self, obj):
        return obj.challenge.duration
    get_duration.short_description = 'Challenge Duration'
    get_duration.admin_order_field = 'challenge__duration'

admin.site.register(DiabetesChallenge, DiabetesChallengeAdmin)
admin.site.register(DiabetesChallengeImage, DiabetesChallengeImageAdmin)
    
    
    
    
    
    
class BloodpressureChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'duration', 'start_date')
    list_filter = ('duration',)
    search_fields = ('user__username',)

class BloodpressureChallengeImageAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_duration', 'day', 'uploaded_at')
    list_filter = ('challenge__duration', 'day')
    search_fields = ('challenge__user__username',)
    ordering = ('challenge__user', 'challenge__duration', 'day')

    def get_user(self, obj):
        return obj.challenge.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'challenge__user'

    def get_duration(self, obj):
        return obj.challenge.duration
    get_duration.short_description = 'Challenge Duration'
    get_duration.admin_order_field = 'challenge__duration'
    
admin.site.register(BloodpressureChallenge, BloodpressureChallengeAdmin)
admin.site.register(BloodpressureChallengeImage, BloodpressureChallengeImageAdmin)

  
  
  
  
   
admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(DiabetesCheck, DiabetesCheckAdmin)
admin.site.register(BloodPressureCheck, BloodPressureCheckAdmin)

admin.site.register(SkinCareCheck, SkinCareCheckAdmin)


    
from .models import WaterIntake

class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_liters', 'date')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)
    ordering = ('-date',)

admin.site.register(WaterIntake, WaterIntakeAdmin)


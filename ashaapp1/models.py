# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class FoodAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_image = models.ImageField(upload_to='food_images/')
    food_item = models.CharField(max_length=255, default='apple')
    calories = models.IntegerField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    servings = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_item} - {self.user.username} - {self.created_at}"

class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_activity = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)

    @classmethod
    def update_last_activity(cls, user):
        activity, created = cls.objects.get_or_create(user=user)
        activity.last_activity = timezone.now()
        activity.is_online = True
        activity.save()

    @classmethod
    def mark_offline(cls, user):
        try:
            activity = cls.objects.get(user=user)
            activity.is_online = False
            activity.save()
        except cls.DoesNotExist:
            pass


class DailyCheckIn(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    check_in_count = models.PositiveIntegerField(default=0)

    def reset_count(self):
        self.check_in_count = 0
        self.save()


class UserProfile(models.Model):
    USER_ROLES = [
        ('user', 'User'),
        ('nutritionist', 'Nutritionist'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')

    def __str__(self):
        return self.user.email if self.user else str(self.email_token)
    
    
    
class DiabetesCheck(models.Model):
    glucose_level = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=100)
    
    
class BloodPressureCheck(models.Model):
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=100)
    
    
    
class SkinCareCheck(models.Model):
    SKIN_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('dry', 'Dry'),
        ('oily', 'Oily'),
        ('combination', 'Combination'),
        ('sensitive', 'Sensitive'),
    ]
    
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES)
    concerns = models.TextField()
    check_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Skin Care Check on {self.check_date.strftime('%Y-%m-%d %H:%M')}"

    
class DiabetesChallenge(models.Model):
    DURATION_CHOICES = [
        (30, '30 Days'),
        (60, '60 Days'),
        (90, '90 Days'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    start_date = models.DateField()

    class Meta:
        unique_together = ['user', 'duration']

class DiabetesChallengeImage(models.Model):
    challenge = models.ForeignKey(DiabetesChallenge, on_delete=models.CASCADE, related_name='images', null=True)
    day = models.IntegerField()
    image = CloudinaryField('image', folder='diabetes_challenge')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['challenge', 'day']

    def get_image_url(self):
        return self.image.url if self.image else None
        
        
class BloodpressureChallenge(models.Model):
    DURATION_CHOICES = [
        (30, '30 Days'),
        (60, '60 Days'),
        (90, '90 Days'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    start_date = models.DateField()

    class Meta:
        unique_together = ['user', 'duration']

class BloodpressureChallengeImage(models.Model):
    challenge = models.ForeignKey(BloodpressureChallenge, on_delete=models.CASCADE, related_name='bloodpressure_images', null=True)
    day = models.IntegerField()
    image = CloudinaryField('image', folder='bloodpressure_challenge')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['challenge', 'day']
        
    def get_image_url(self):
        return self.image.url if self.image else None
        
    
    
    
class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_liters = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.total_liters} liters on {self.date.date()}"
    
    
    


class ExerciseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    blood_sugar_before = models.IntegerField()
    blood_sugar_after = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

class WeeklyStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    exercise_minutes = models.IntegerField(default=0)
    glucose_stability = models.FloatField(default=0)  # percentage
    active_days = models.IntegerField(default=0)
    energy_level = models.FloatField(default=0)


class BloodPressureExerciseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=50, choices=[
        ('Low-Impact Cardio', 'Low-Impact Cardio'),
        ('Breathing Exercises', 'Breathing Exercises'),
        ('Flexibility & Stretching', 'Flexibility & Stretching')
    ])
    duration = models.IntegerField(help_text='Exercise duration in minutes')
    
    # Subjective Blood Pressure Assessment
    feeling_after_exercise = models.CharField(max_length=50, choices=[
        ('great', 'Great (likely BP improvement)'),
        ('normal', 'Normal (no significant change)'),
        ('slightly_tired', 'Slightly Tired (potential BP elevation)'),
        ('dizzy', 'Dizzy or Fatigued (potential BP elevation)')
    ])
    activity_intensity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High')
    ])
    stress_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High')
    ])
    
    # Symptoms
    YES_NO_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    headache = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    light_headedness = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    palpitations = models.CharField(max_length=3, choices=YES_NO_CHOICES)
    
    # Energy Boost
    energy_boost = models.IntegerField(help_text='Perceived energy boost (1-10)', 
                                       validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} - {self.date.date()}"

    class Meta:
        ordering = ['-date']
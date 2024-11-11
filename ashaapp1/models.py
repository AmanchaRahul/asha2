# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verified = models.BooleanField(default=False)

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
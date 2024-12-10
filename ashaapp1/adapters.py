from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # Skip the intermediate page and allow auto signup
        return True

    def save_user(self, request, sociallogin, form=None):
        # Call the parent method to create or update the user
        user = super().save_user(request, sociallogin, form)
        
        # Check if the user already has a profile
        if not hasattr(user, 'userprofile'):
            # Create a new UserProfile with 'user' role
            from .models import UserProfile  # Import your UserProfile model
            UserProfile.objects.create(user=user, role='user')
        
        return user

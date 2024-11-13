# adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email_at_domain

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # Allow auto signup for Google users
        return True  # Allow signup automatically if the user doesn't exist

    def pre_social_login(self, request, sociallogin):
        """
        This is called before the login process.
        We can use it to customize the login/signup behavior.
        """
        user = sociallogin.user

        # Check if the user already exists by email and log them in directly if they do
        if user_email_at_domain(user.email):
            try:
                existing_user = self.get_account(user.email)
                sociallogin.user = existing_user
            except User.DoesNotExist:
                pass  # If user doesn't exist, it'll go through the signup process
        return sociallogin


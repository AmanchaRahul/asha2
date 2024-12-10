from ashaapp1.models import UserProfile

def set_user_role(strategy, details, user=None, *args, **kwargs):
    """
    Ensure users logging in via Google OAuth are assigned the 'user' role.
    """
    if user:
        # Check if the user already has a profile
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Assign 'user' role if it's not set or if the profile is newly created
        if created or not user_profile.role:
            user_profile.role = 'user'
            user_profile.save()

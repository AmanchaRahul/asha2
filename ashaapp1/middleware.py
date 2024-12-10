from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from .models import UserActivity 


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update last activity for logged-in users
        if request.user and not isinstance(request.user, AnonymousUser):
            from .models import UserActivity  # Import here to avoid circular import
            UserActivity.update_last_activity(request.user)

        response = self.get_response(request)
        return response
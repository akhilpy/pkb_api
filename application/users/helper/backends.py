from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class MobileBackend(ModelBackend):
    """
    This backed has been introduced for mobile no based user
    authentication, which will be consumed by authenticate
    function.
    """
    def authenticate(self,  mobile=None, otp=None):
        User = get_user_model()
        try:
            user_object = User.objects.get(mobile=mobile)
            if user_object.otp==otp:
                return user_object
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
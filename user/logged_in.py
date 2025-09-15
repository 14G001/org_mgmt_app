from django.contrib.auth.models import AnonymousUser

def is_user_logged_in(request):
    return not isinstance(request.user, AnonymousUser)
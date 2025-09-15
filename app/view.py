from django.views import View
from user.logged_in import is_user_logged_in
from django.shortcuts import redirect
from security.urls import is_url_secure
from app.responses import resource_not_exists
from app.settings import APP_VERSION

class UiView(View):
    def dispatch(self, request, *args, **kwargs):
        if (APP_VERSION != "example"
            and not is_user_logged_in(request)):
            next_url = request.get_full_path()
            last_url_part = ''
            if (not '/' == next_url 
                and is_url_secure(next_url)):
                last_url_part = f'?next_url={next_url}'
            return redirect(f'/login/{last_url_part}')
        return super().dispatch(request, *args, **kwargs)

class SecureView(View):
    def validate_message(self, request):
        return None
    def dispatch(self, request, *args, **kwargs):
        if (APP_VERSION != "example"
            and not is_user_logged_in(request)):
            return resource_not_exists() # For security reasons; this endpoints should not reveal its existance to not logged users.
        error_response = self.validate_message(request)
        if None != error_response:
            return error_response
        return super().dispatch(request, *args, **kwargs)
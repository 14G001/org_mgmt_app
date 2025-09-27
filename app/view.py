from django.views import View
from user.logged_in import is_user_logged_in
from django.shortcuts import redirect
from security.urls import is_url_secure
from app.responses import resource_not_exists, access_denied
from app.settings import AVAILABLE_APPS, EXAMPLE_APP_INDICATOR

class AppView(View):
    def validate_app(self, request, app):
        user = request.user
        if (not app.endswith(EXAMPLE_APP_INDICATOR)
            and user.is_authenticated
            and user.app.name != app):
            return access_denied()
        if app not in AVAILABLE_APPS:
            return resource_not_exists()
        return None

class UiView(AppView):
    def dispatch(self, request, app, *args, **kwargs):
        error = self.validate_app(request, app)
        if error != None:
            return error
        if (not app.endswith(EXAMPLE_APP_INDICATOR)
            and not is_user_logged_in(request)):
            next_url = request.get_full_path()[len("/")+len(app):]
            last_url_part = ''
            if ('/' != next_url 
                and is_url_secure(next_url)):
                last_url_part = f'?next_url={next_url}'
            print(f"FINAL URL: {f'/{app}/login/{last_url_part}'}")
            return redirect(f'/{app}/login/{last_url_part}')
        return super().dispatch(request, app, *args, **kwargs)

class SecureView(AppView):
    def validate_message(self, request):
        return None
    def dispatch(self, request, app, *args, **kwargs):
        error = self.validate_app(request, app)
        if error != None:
            return error
        if (not app.endswith(EXAMPLE_APP_INDICATOR)
            and not is_user_logged_in(request)):
            return resource_not_exists() # For security reasons; this endpoints should not reveal its existance to not logged users.
        error_response = self.validate_message(request)
        if None != error_response:
            return error_response
        return super().dispatch(request, app, *args, **kwargs)
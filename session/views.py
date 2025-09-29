from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from security.urls import is_url_secure
from user.logged_in import is_user_logged_in
from app.responses import ok, error, resource_not_exists
from app.render import template
from app.view import AppView
from app.apps.info import EXAMPLE_APP_INDICATOR
from user.settings import USER_APPS
from app.test_values.user import TEST_USERS_PASSWORD
import json

class TestLoginView(AppView):
    def get(self, request, app):
        is_users_app = app in USER_APPS
        is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
        if not (is_users_app and is_example_app):
            return resource_not_exists()
        return template(request, app, "test_login.html")
    def post(self, request, app):
        is_users_app = app in USER_APPS
        is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
        if not (is_users_app and is_example_app):
            return resource_not_exists()
        data = json.loads(request.body)
        user = authenticate(
            request,
            username=f"{app}/{data.get('username')}",
            password=TEST_USERS_PASSWORD
        )
        login(request, user)
        return ok()

class LoginView(AppView):
    def redirect_to_original_url(self, request):
        next_url = request.GET.get('next_url')
        if (None == next_url
            or not is_url_secure(next_url)):
            next_url = '/'
        print(f"REDIRECT 2> {next_url}")
        return redirect(next_url)
    def should_login(self, request, app):
        is_users_app = app in USER_APPS
        is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
        return not (
            (is_example_app and not is_users_app)
            or is_user_logged_in(request))
    def get(self, request, app):
        req_err = self.validate_app(request, app)
        if req_err != None:
            return req_err
        if not self.should_login(request, app):
            return self.redirect_to_original_url(request)
        is_users_app = app in USER_APPS
        is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
        if is_users_app and is_example_app:
            return redirect(f"/{app}/test_login/")
        return template(request, app, 'login.html')
    def post(self, request, app):
        req_err = self.validate_app(request, app)
        if req_err != None:
            return req_err
        if is_user_logged_in(request):
            return ok()
        data = json.loads(request.body)
        user = authenticate(
            request,
            username=f"{app}/{data.get('username')}",
            password=data.get('password')
        )
        if user is not None:
            login(request, user) # Creates session and cookie automatically
            return ok()
        return error(401, 'invalid credentials')
    
class LogoutView(AppView):
    def post(self, request, app):
        req_err = self.validate_app(request, app)
        if req_err != None:
            return req_err
        if (app.endswith(EXAMPLE_APP_INDICATOR)
            and app not in USER_APPS):
            return error(500, "Example app version")
        logout(request) # Removes session from server
        return ok()
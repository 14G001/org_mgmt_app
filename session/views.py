from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from security.urls import is_url_secure
from user.logged_in import is_user_logged_in
from app.responses import ok, error
from app.render import send_template
from app.view import AppView
import json

class LoginView(AppView):
    def redirect_to_original_url(self, request):
        next_url = request.GET.get('next_url')
        if (None == next_url
            or not is_url_secure(next_url)):
            next_url = '/'
        print(f"REDIRECT 2> {next_url}")
        return redirect(next_url)
    def get(self, request, app):
        req_err = self.validate_app(app)
        if req_err != None:
            return req_err
        if (app.endswith(EXAMPLE_APP_INDICATOR)
            or is_user_logged_in(request)):
            return self.redirect_to_original_url(request)
        return send_template(request, app, 'login.html')
    def post(self, request, app):
        req_err = self.validate_app(app)
        if req_err != None:
            return req_err
        if is_user_logged_in(request):
            return ok()
        data = json.loads(request.body)
        user = authenticate(
            request,
            username=data.get('username'),
            password=data.get('password')
        )
        if user is not None:
            login(request, user) # Creates session and cookie automatically
            return ok()
        return error(401, 'invalid credentials')
    
class LogoutView(AppView):
    def post(self, request, app):
        req_err = self.validate_app(app)
        if req_err != None:
            return req_err
        if app.endswith(EXAMPLE_APP_INDICATOR):
            return error(500, "Example app version")
        logout(request) # Removes session from server
        return ok()
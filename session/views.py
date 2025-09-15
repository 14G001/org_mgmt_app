from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from security.urls import is_url_secure
from user.main_user import create_main_user_if_not_exists
from user.logged_in import is_user_logged_in
from app.responses import ok, error
import json

class LoginView(View):
    def redirect_to_original_url(self, request):
        next_url = request.GET.get('next_url')
        if (None == next_url
            or not is_url_secure(next_url)):
            next_url = '/'
        print(f"REDIRECT 2> {next_url}")
        return redirect(next_url)
    def get(self, request):
        if is_user_logged_in(request):
            return self.redirect_to_original_url(request)
        return render(request, 'login.html')
    def post(self, request):
        if is_user_logged_in(request):
            return ok()
        create_main_user_if_not_exists()
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
    
class LogoutView(View):
    def post(self, request):
        logout(request) # Removes session from server
        return ok()
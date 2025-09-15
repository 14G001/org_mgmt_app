from django.shortcuts import render
from app.settings import APP_VERSION

TITLE = "ONG Admin" if APP_VERSION != "example" else "ONG Admin Example Version"

def send_template(request, path):
    return render(request, path, {"title":TITLE})
from django.shortcuts import render
from app.settings import EXAMPLE_APP_INDICATOR

def send_template(request, app, path):
    title = None
    is_example_app_version = app.endswith(EXAMPLE_APP_INDICATOR)
    if is_example_app_version:
        title = "ONG Admin Example Version"
    else:
        title = "ONG Admin"
    return render(request, path, {
        "title":title, "example_version":is_example_app_version})
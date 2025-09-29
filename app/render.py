from django.shortcuts import render
from app.apps.info import EXAMPLE_APP_INDICATOR, AVAILABLE_APPS

def template(request, app, path):
    title = None
    if app.startswith("org_mgmt_app"):
        title = "ONG Admin"
    else:
        title = AVAILABLE_APPS[app]["title"]
    return render(request, path, {
        "title":title, "example_version":app.endswith(EXAMPLE_APP_INDICATOR)})
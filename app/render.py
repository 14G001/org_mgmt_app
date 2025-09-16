from django.shortcuts import render
from app.settings import ORG_MGMT_APP

def send_template(request, app, path):
    title = None
    if app == ORG_MGMT_APP:
        title = "ONG Admin"
    else:
        title = "ONG Admin Example Version"
    return render(request, path, {
        "title":title, "example_version":app != ORG_MGMT_APP})
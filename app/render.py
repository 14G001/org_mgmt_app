from django.shortcuts import render
from app.settings import EXAMPLE_APP_INDICATOR, AVAILABLE_APPS

def send_template(request, app, path):
    is_example_app_version = app.endswith(EXAMPLE_APP_INDICATOR)
    app_name = None
    if app.startswith("org_mgmt_app"):
        app_name = "ONG"
    else:
        app_name = AVAILABLE_APPS[app]["name"]
    title = f"{app_name} Admin"
    if is_example_app_version:
        title += " - Versión de Ejemplo"
    return render(request, path, {
        "title":title, "example_version":is_example_app_version})
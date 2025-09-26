from django.shortcuts import render
from app.settings import EXAMPLE_APP_INDICATOR, ORG_MGMT_APP_EXA

def send_template(request, app, path):
    is_example_app_version = app.endswith(EXAMPLE_APP_INDICATOR)
    app_name = "Enseñá X Argentina" if app.startswith(ORG_MGMT_APP_EXA) else None
    title = f"{app_name} Admin"
    if is_example_app_version:
        title += " - Versión de Ejemplo"
    return render(request, path, {
        "title":title, "example_version":is_example_app_version})
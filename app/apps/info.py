from org_mgmt_app.settings import get_org_mgmt_app_info
from ensenaxargentina.settings import get_ensenaxargentina_app_info

EXAMPLE_APP_INDICATOR = '_example'

def get_app_versions(**kwargs):
    available_apps = {}
    for app in kwargs:
        app_settings = kwargs[app]
        available_apps[app                            ] = app_settings
        example_app_version_data = app_settings.copy()
        title = example_app_version_data["title"]
        example_app_version_data["title"] = f"{title} - Versión de Ejemplo"
        available_apps[f"{app}{EXAMPLE_APP_INDICATOR}"] = example_app_version_data
    return available_apps
AVAILABLE_APPS = get_app_versions(
    org_mgmt_app     = get_org_mgmt_app_info("Organización Actual"),
    exa_org_mgmt_app = get_org_mgmt_app_info("Enseñá X Argentina Admin" ),
    ensenaxargentina = get_ensenaxargentina_app_info()             ,
)
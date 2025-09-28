from org_mgmt_app.settings import get_org_mgmt_app_info
from ensenaxargentina.settings import get_ensenaxargentina_app_info

EXAMPLE_APP_INDICATOR = '_example'

def get_app_versions(**kwargs):
    available_apps = {}
    for app in kwargs:
        available_apps[app                            ] = kwargs[app]
        available_apps[f"{app}{EXAMPLE_APP_INDICATOR}"] = kwargs[app]
    return available_apps
AVAILABLE_APPS = get_app_versions(
    org_mgmt_app     = get_org_mgmt_app_info("Organización Actual"),
    exa_org_mgmt_app = get_org_mgmt_app_info("Enseñá X Argentina" ),
    ensenaxargentina = get_ensenaxargentina_app_info()             ,
)

USERS_APP = "ensenaxargentina"
from app.apps.info import AVAILABLE_APPS, EXAMPLE_APP_INDICATOR

APP_TYPE_ORG_MGMT_APP = 0
APP_TYPE_EXA          = 1

def get_org_mgmt_apps():
    org_mgmt_apps = {}
    for app_name in ["org_mgmt_app", "exa_org_mgmt_app"]:
        example_app_version_name = f"{app_name}{EXAMPLE_APP_INDICATOR}"
        org_mgmt_apps[app_name                ] = AVAILABLE_APPS[app_name                ]
        org_mgmt_apps[example_app_version_name] = AVAILABLE_APPS[example_app_version_name]
    return org_mgmt_apps
ORG_MGMT_APPS = get_org_mgmt_apps()

def get_app_type(app):
    if app in ORG_MGMT_APPS:
        return APP_TYPE_ORG_MGMT_APP
    return APP_TYPE_EXA
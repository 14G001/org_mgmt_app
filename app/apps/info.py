from org_mgmt_app.settings import get_org_mgmt_app_info
from campus      .settings import get_campus_app_info

EXAMPLE_APP_INDICATOR = '_example'

def get_app_versions(**kwargs):
    available_apps = {}
    for app in kwargs:
        app_settings = kwargs[app]
        app_user_types = app_settings["user_types"]
        for user_type_name in app_user_types:
            user_type_permissons = app_user_types[user_type_name]["permissons"]
            app_elm_user_type = user_type_permissons.get("user_type")
            if None != app_elm_user_type:
                app_elm_user_type["app_filter"] = "app"
            app_elm_user      = user_type_permissons.get("user")
            if None != app_elm_user:
                app_elm_user     ["app_filter"] = "app"
        available_apps[app] = app_settings
        example_app_version_data = app_settings.copy()
        title = example_app_version_data["title"]
        example_app_version_data["title"] = f"{title} - Versión de Ejemplo"
        available_apps[f"{app}{EXAMPLE_APP_INDICATOR}"] = example_app_version_data
    return available_apps
AVAILABLE_APPS = get_app_versions(
    org_mgmt_app     = get_org_mgmt_app_info("Organización Actual"      ),
    exa_org_mgmt_app = get_org_mgmt_app_info("Enseñá X Argentina Admin" ),
    campus           = get_campus_app_info()                             ,
)

def get_user_type_settings(app, user_type):
    return AVAILABLE_APPS[app]["user_types"][user_type]
def get_user_permissons(app, user_type):
    return get_user_type_settings(app, user_type)["permissons"]
from utils.dictionary import do_dictionary_group_have_same_keys
from campus.user_types.settings   import APP_USER_TYPE_SETTINGS
from campus.user_types.permissons import APP_USER_TYPE_PERMISSONS
from campus.user_types.view       import APP_USER_TYPE_VIEWS

APP_TITLE = "Campus"

def get_campus_app_info():
    user_types = {}
    app_info = {
        "title": APP_TITLE,
        "user_types": user_types,
    }
    if not do_dictionary_group_have_same_keys(
        APP_USER_TYPE_SETTINGS, APP_USER_TYPE_PERMISSONS, APP_USER_TYPE_VIEWS):
        raise f"ERROR: Some user types settings, permissons or views has not been set on app {APP_TITLE}."
    for user_type in APP_USER_TYPE_SETTINGS:
        user_types[user_type] = APP_USER_TYPE_SETTINGS[user_type]
    for user_type in APP_USER_TYPE_PERMISSONS:
        user_types[user_type]["permissons"] = APP_USER_TYPE_PERMISSONS[user_type]
    for user_type in APP_USER_TYPE_VIEWS:
        user_types[user_type]["view"      ] = APP_USER_TYPE_VIEWS[user_type]
    return app_info
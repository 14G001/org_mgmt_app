from user.settings import USER_TYPE_MODEL, USER_MODEL

def get_user_type_permissons(app_section_types, default_app_elm_settings):
    # This should obtain data directly without using AVAILABLE_APPS element to avoid circular imports
    def_usr_prmsns = {}
    for app_elm in app_section_types:
        def_usr_prmsns[app_elm.type] = default_app_elm_settings
    return def_usr_prmsns
def get_admin_permissons(app_section_types):
    admin_permissons = get_user_type_permissons(app_section_types, {"actions":"cud"})
    if "user_type" in admin_permissons:
        admin_permissons["user_type"] = {
            "actions"   :""   ,
            "app_filter":"app",
        }
    if "user" in admin_permissons:
        admin_permissons["user"] = {
            "actions"   :"cud",
            "app_filter":"app",
        }
    return admin_permissons
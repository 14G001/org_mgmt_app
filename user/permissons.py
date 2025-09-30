from django.db.models import Q

def get_user_type_permissons(app_section_types, default_app_elm_settings):
    # This should obtain data directly without using AVAILABLE_APPS element to avoid circular imports
    def_usr_prmsns = {}
    for app_elm in app_section_types:
        def_usr_prmsns[app_elm.type] = default_app_elm_settings.copy()
    return def_usr_prmsns
def set_user_models_permissons(app_section_types, user_types_to_exclude):
    user_type_permissons = get_user_type_permissons(app_section_types, {"actions":"cud"})
    app_elm_user_type = user_type_permissons.get("user_type")
    if None != app_elm_user_type:
        app_elm_user_type["actions"] = ""
        app_elm_user_type["filter" ] = ~Q(name__in=user_types_to_exclude)
    app_elm_user = user_type_permissons.get("user")
    if None != app_elm_user:
        app_elm_user["actions"] = "cud"
        app_elm_user["filter" ] = ~Q(type__name__in=user_types_to_exclude)
    return user_type_permissons

def get_root_user_settings(app_section_types):
    return {
        "title":"Root",
        "permissons":set_user_models_permissons(app_section_types, ["root"        ]),
    }
def get_admin_user_settings(app_section_types):
    return {
        "title":"Admin",
        "permissons":set_user_models_permissons(app_section_types, ["root","admin"]),
    }
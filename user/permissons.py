def get_app_complete_user_permissons(app_section_types):
    def_usr_prmsns = {}
    for section_type in [app_elm.type for app_elm in app_section_types]: # This should be done that way to avoid circular imports
        def_usr_prmsns[section_type] = {"actions":"crud"}
    return def_usr_prmsns
from user.permissons import get_user_type_permissons
from org_mgmt_app.elements import ORG_MGMT_APP_ELMS_INFO

ORG_MGMT_APP_DEFAULT_USER_PERMISSONS = get_user_type_permissons(
    ORG_MGMT_APP_ELMS_INFO, {"actions":"crud"})

def get_org_mgmt_app_info(title):
    return {
        "title":title,
        "user_types": {
            "default_user": {
                "title": "Default",
                "permissons": ORG_MGMT_APP_DEFAULT_USER_PERMISSONS
            }
        }
    }
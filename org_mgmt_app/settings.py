from user.permissons import get_app_complete_user_permissons
from org_mgmt_app.elements import ORG_MGMT_APP_ELMS_INFO

ORG_MGMT_APP_DEFAULT_USER_PERMISSONS = get_app_complete_user_permissons(ORG_MGMT_APP_ELMS_INFO)

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
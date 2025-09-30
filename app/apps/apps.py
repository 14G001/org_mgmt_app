from app.apps.type import get_app_type, APP_TYPE_ORG_MGMT_APP
from org_mgmt_app.elements import ORG_MGMT_APP_ELMS_INFO
from campus      .elements import CAMPUS_APP_ELMS_INFO

def get_app_elms_info_source(app):
    if APP_TYPE_ORG_MGMT_APP == get_app_type(app):
        return ORG_MGMT_APP_ELMS_INFO
    return CAMPUS_APP_ELMS_INFO
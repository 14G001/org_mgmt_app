from org_mgmt_app.test_values import init_org_mgmt_app_db_test_values
from campus      .test_values import init_campus_db_test_values
from app.apps.type import get_app_type, APP_TYPE_ORG_MGMT_APP

def init_db_test_values(app):
    if APP_TYPE_ORG_MGMT_APP == get_app_type(app):
        init_org_mgmt_app_db_test_values(app)
        return
    init_campus_db_test_values(app)
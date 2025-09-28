from app.view import UiView, SecureView
from app.responses import ok
from app.render import send_template
from org_mgmt_app.views.utils.list_item_fields import get_item_list_section
from app.app.elements import get_app_section_types

class AppHomeView(UiView):
    def get(self, request, app):
        return send_template(request, app, 'admin.html')

class HomeItemsView(SecureView):
    def get(self, request, app):
        sections = []
        for list_item_section in get_app_section_types(app):
            sections.append(get_item_list_section(app, list_item_section))
        return ok(sections=sections)
        
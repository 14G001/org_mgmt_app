from app.view import UiView, SecureView
from app.responses import ok
from app.render import send_template
from organization.views.utils.list_item_fields import get_item_list_section
from organization.test_values.init import init_organization_test_values
from organization.elements.elements import get_org_elms_public_info

SECTION_TYPES = list(get_org_elms_public_info().keys())

class HomeView(UiView):
    def get(self, request):
        return send_template(request, 'admin.html')

class HomeItemsView(SecureView):
    def get(self, request):
        init_organization_test_values()
        sections = []
        for list_item_section in SECTION_TYPES:
            sections.append(get_item_list_section(list_item_section))
        return ok(sections=sections)
        
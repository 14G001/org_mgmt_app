from app.view import UiView, SecureView
from app.responses import ok
from app.render import template
from app.views.utils.list_item_fields import get_item_list_section
from app.app.elements import get_app_section_types

class HomeView(UiView):
    def get(self, request, app):
        return template(request, app, 'admin.html')

class HomeItemsView(SecureView):
    def get(self, request, app):
        sections = []
        for list_item_section in get_app_section_types(app):
            section = get_item_list_section(request, app, list_item_section)
            if None != section:
                sections.append(section)
        return ok(sections=sections)
        
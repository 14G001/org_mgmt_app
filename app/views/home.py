from app.view import UiView, SecureView
from app.responses import ok
from app.render import template
from app.views.utils.list_item_fields import get_item_list_section
from app.apps.info import get_user_type_settings

class HomeView(UiView):
    def get(self, request, app):
        return template(request, app, 'admin.html')

class HomeItemsView(SecureView):
    def get(self, request, app):
        user_type = self.user_type
        user_type_settings = get_user_type_settings(app, user_type)
        user_type_app_elm_permissons = user_type_settings["permissons"]
        user_type_app_elm_settings   = user_type_settings.get("settings", {})
        sections = []
        for app_elm_type in list(user_type_app_elm_permissons.keys()):
            app_elm_settings = user_type_app_elm_settings.get(app_elm_type)
            if (None == app_elm_settings
                or False != app_elm_settings.get("display_at_home")):
                section = get_item_list_section(
                    request, app, user_type, app_elm_type)
                if None != section:
                    sections.append(section)
        return ok(sections=sections)
        
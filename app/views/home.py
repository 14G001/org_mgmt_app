from app.view import UiView, SecureView
from app.responses import ok
from app.render import template
from app.views.utils.list_item_fields import get_item_list_section
from user.models import User
from app.apps.info import AVAILABLE_APPS

class HomeView(UiView):
    def get(self, request, app):
        return template(request, app, 'admin.html')

class HomeItemsView(SecureView):
    def get(self, request, app):
        user_type = User.objects.get_type(request)
        user_type_app_elm_permissons = (AVAILABLE_APPS
            [app]["user_types"][user_type]["permissons"])
        sections = []
        for app_elm_type in list(user_type_app_elm_permissons.keys()):
            print("APP ELM TYPE")
            print(app_elm_type)
            user_type_app_elm_settings = user_type_app_elm_permissons[app_elm_type].get("settings")
            if (None == user_type_app_elm_settings
                or False != user_type_app_elm_settings.get("display_at_home")):
                section = get_item_list_section(
                    request, app, app_elm_type, user_type=user_type)
                if None != section:
                    sections.append(section)
        return ok(sections=sections)
        
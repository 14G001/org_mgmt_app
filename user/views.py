from app.view import SecureView
from app.apps.info import EXAMPLE_APP_INDICATOR
from user.settings import USER_APPS
from app.responses import resource_not_exists, ok
from user.models import User
from app.views.utils.list_item_fields import get_items_list

class TestUsersView(SecureView):
    def get(self, request, app):
        is_users_app = app in USER_APPS
        is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
        if not (is_users_app and is_example_app):
            return resource_not_exists()
        request.user = User.objects.filter(
            type__app__name=app, type__name="admin").first()
        print("USER")
        print(request.user)
        users = get_items_list(request, app, "user", [], ["username","name","type"])
        print(users)
        return ok(
            users=users)
from app.view import SecureView
from app.apps.info import EXAMPLE_APP_INDICATOR, AVAILABLE_APPS
from user.settings import USER_APPS
from app.responses import resource_not_exists, ok
from user.models import User

class TestUsersView(SecureView):
    def get(self, request, app):
        is_users_app = app in USER_APPS
        is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
        if not (is_users_app and is_example_app):
            return resource_not_exists()
        users = []
        for user_type in list(AVAILABLE_APPS[app]["user_types"].keys()):
            users += list(User.objects.filter(
                type__app__name=app, type__name=user_type)
                .values_list("username","name","type__title"))
        return ok(users=users)
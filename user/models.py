import django.db.models as m
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from user.types import USER_TYPES
from app.settings import AVAILABLE_APPS

def init_type_model(final_items, model, item_types):
    if final_items != None:
        return final_items
    db_items = [item[0] for item in list(model.objects.values_list("name"))]
    for local_item in item_types:
        if local_item not in db_items:
            model.objects.create(name=local_item)
    items = {}
    for item in model.objects.all():
        items[item.name] = item
    return items

class App(m.Model):
    name = m.TextField(unique=True)
apps = None
def init_apps():
    global apps
    apps = init_type_model(apps, App, AVAILABLE_APPS)

class UserType(m.Model):
    name = m.TextField(unique=True)
user_types = None
def init_user_types():
    global user_types
    user_types = init_type_model(user_types, UserType, USER_TYPES)


class CustomUserManager(BaseUserManager):
    def init_user(self, app_name, email, username, password, user_type):
        init_apps()
        init_user_types()
        email = self.normalize_email(email)
        user  = self.model(
            app=apps[app_name],
            email=email, username=username, identifier=f"{app_name}/{email}",
            type=UserType.objects.get(name=user_type))
        user.set_password(password)
        return user
    def create_user(self, app, email, username, password, user_type="client"):
        user = self.init_user(app, email, username, password, user_type)
        user.save(using=self._db)
    def create_superuser(self, app, email, username, password, user_type="client"):
        user = self.init_user(app, email, username, password, user_type)
        user.is_staff     = True
        user.is_superuser = True
        user.type         = UserType.objects.get(name="complete_control")
        user.save(using=self._db)

class User(AbstractBaseUser, PermissionsMixin):
    app        = m.ForeignKey(App, null=False, on_delete=m.CASCADE)
    email      = m.EmailField()
    username   = m.CharField(max_length=150)
    type       = m.ForeignKey(UserType, null=False, on_delete=m.CASCADE)
    identifier = m.CharField(max_length=300, null=False, unique=True)
    objects    = CustomUserManager()
    # Default Django fields:
    is_active    = m.BooleanField(default=True)
    is_staff     = m.BooleanField(default=False)
    is_superuser = m.BooleanField(default=False)
    USERNAME_FIELD  = "identifier"
    REQUIRED_FIELDS = ["app","email"]
    # App isolators:
    class Meta:
        unique_together = (("app","email"),("app","username"),)
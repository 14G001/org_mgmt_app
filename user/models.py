from app.model import AppModel, AppModelManager
import django.db.models as m
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from app.apps.info import AVAILABLE_APPS

class App(AppModel):
    name = m.TextField(unique=True)
apps = None
def init_apps():
    global apps
    if apps != None:
        return
    db_apps = [item[0] for item in list(App.objects.values_list("name"))]
    for local_item in AVAILABLE_APPS:
        if local_item not in db_apps:
            App.objects.create(name=local_item)
    apps = {}
    for item in App.objects.all():
        apps[item.name] = item

class UserType(AppModel):
    app   = m.ForeignKey(App, null=False, on_delete=m.CASCADE)
    value = m.TextField()
    class Meta:
        unique_together = (("app","value",),)
user_types_x_app = None
def init_user_types_x_app():
    global user_types_x_app
    if user_types_x_app != None:
        return
    db_user_types = [f"{item[0]}/{item[1]}" for item in list(UserType.objects.values_list("app__name","value"))]
    print("db user types")
    print(db_user_types)
    print(list(AVAILABLE_APPS.keys()))
    for app_name in AVAILABLE_APPS:
        app_info = AVAILABLE_APPS[app_name]
        for user_type in app_info["user_types"]:
            user_type_key = f"{app_name}/{user_type}"
            if user_type_key not in db_user_types:
                UserType.objects.create(app=apps[app_name], value=user_type)
    user_types_x_app = {}
    for item in UserType.objects.select_related("app").all():
        app_name = item.app.name
        app_usr_types =  user_types_x_app.get(app_name)
        if None == app_usr_types:
            app_usr_types = {}
            user_types_x_app[app_name] = app_usr_types
        app_usr_types[item.value] = item

class CustomUserManager(AppModelManager, BaseUserManager):
    def init_user(self, app_name, email, username, password, user_type):
        init_apps()
        init_user_types_x_app()
        email = self.normalize_email(email)
        user  = self.model(
            app=apps[app_name],
            email=email, username=username, identifier=f"{app_name}/{username}",
            type=UserType.objects.get(app=apps[app_name], value=user_type))
        user.set_password(password)
        return user
    def create_user(self, app, email, username, password, user_type):
        user = self.init_user(app, email, username, password, user_type)
        user.save(using=self._db)
        return user
    def create_superuser(self, app, email, username, password, user_type):
        user = self.init_user(app, email, username, password, user_type)
        user.is_staff     = True
        user.is_superuser = True
        user.type         = UserType.objects.get(name="complete_control")
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    app        = m.ForeignKey(App, null=False, on_delete=m.CASCADE)
    email      = m.EmailField(null=False)
    username   = m.CharField(max_length=150, null=False)
    type       = m.ForeignKey(UserType, null=False, on_delete=m.CASCADE)
    identifier = m.CharField(max_length=300, null=False, unique=True)
    phone      = m.CharField(max_length=80 , null=True , unique=True)
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
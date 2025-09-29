import django.db.models as m
from user.settings import USER_APPS

class AppQuerySet(m.QuerySet):
    def using(self, alias):
        if alias in USER_APPS:
            alias = "default"
        return super().using(alias)
class AppModelManager(m.Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db)
class AppModel(m.Model):
    objects = AppModelManager()
    class Meta:
        abstract = True
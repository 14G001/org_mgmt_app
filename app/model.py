import django.db.models as m
from user.settings import USERS_APP

class AppQuerySet(m.QuerySet):
    def using(self, alias):
        if alias.startswith(USERS_APP):
            alias = "default"
        return super().using(alias)
class AppModelManager(m.Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db)
class AppModel(m.Model):
    objects = AppModelManager()
    class Meta:
        abstract = True
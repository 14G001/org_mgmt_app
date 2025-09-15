import django.db.models as m
from organization.models import Person

class User(m.Model):
    name = m.TextField(null=False, unique=True)
    password = m.TextField()
    related_person = m.ForeignKey(Person, null=True, related_name='users', on_delete=m.PROTECT)
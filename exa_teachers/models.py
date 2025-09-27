from utils.common_models import AddressModelBase, PersonModelBase
from user.models import User
import django.db.models as m

class Address(AddressModelBase):
    pass
class School(m.Model):
    address  = m.ForeignKey(Address, null=False, on_delete=m.CASCADE)
class SubjectType(m.Model):
    name    = m.TextField(unique=True)
class Subject(m.Model):
    type       = m.ForeignKey(SubjectType, null=False, on_delete=m.CASCADE)
    school     = m.ForeignKey(School     , null=False, on_delete=m.CASCADE)
    start_date = m.DateField(null=False)
    end_date   = m.DateField(null=False)
class ExamType(m.Model):
    value = m.TextField(unique=True)
class SubjectExam(m.Model):
    subject = m.ForeignKey(Subject , null=False, on_delete=m.CASCADE)
    type    = m.ForeignKey(ExamType, null=False, on_delete=m.CASCADE)
    class Meta:
        unique_together = (("subject","type",),)

class Person(PersonModelBase):
    user  = m.ForeignKey(User, null=False, on_delete=m.CASCADE)
    phone = m.CharField(max_length=80, null=False)
class PersonRoleType(m.Model):
    value = m.TextField(unique=True) # 'Teacher','Student'

class SubjectXTeacher(m.Model):
    subject = m.ForeignKey(Subject, null=False, on_delete=m.CASCADE)
    teacher = m.ForeignKey(Person , null=False, on_delete=m.CASCADE)
    class Meta:
        unique_together = (("subject","teacher",),)

class SubjectXStudent(m.Model):
    subject = m.ForeignKey(Subject, null=False, on_delete=m.CASCADE)
    student = m.ForeignKey(Person , null=False, on_delete=m.CASCADE)
    class Meta:
        unique_together = (("subject","student",),)
class NoteXStudent(m.Model):
    exam    = m.ForeignKey(SubjectExam, null=False, on_delete=m.CASCADE)
    student = m.ForeignKey(Person     , null=False, on_delete=m.CASCADE)
    note    = m.FloatField(null=False)
    class Meta:
        unique_together = (("exam","student",),)


class Form(m.Model):
    title = m.TextField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)
class FormFieldType(m.Model):
    name = m.TextField(unique=True)
class StudentFormField(m.Model):
    form = m.ForeignKey(Form         , null=False, on_delete=m.CASCADE)
    type = m.ForeignKey(FormFieldType, null=False, on_delete=m.CASCADE)
    name = m.TextField(null=False)
    value= m.TextField(null=True ) # Can be null for cases in which person that should complete the form didnt do it or value was not present and not required.
    class Meta:
        unique_together = (("form","name",),)


'''
4 different apps:

Complete control,
Account creation and setting,
Teacher side,
Student side,

'''
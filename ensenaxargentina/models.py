from utils.common_models import AddressModelBase
from user.models import User
from app.model import AppModel
import django.db.models as m

class Address(AddressModelBase):
    pass
class School(AppModel):
    name     = m.TextField(null=False)
    address  = m.ForeignKey(Address, null=False, unique=True, related_name="schools", on_delete=m.CASCADE)
class SubjectType(AppModel):
    name    = m.TextField(unique=True)
class Subject(AppModel):
    school     = m.ForeignKey(School     , null=False, related_name="subjects", on_delete=m.CASCADE)
    type       = m.ForeignKey(SubjectType, null=False, related_name="subjects", on_delete=m.CASCADE)
    title      = m.TextField(null=False)
    start_date = m.DateField(null=False)
    end_date   = m.DateField(null=False)
    class Meta:
        unique_together = (("school","title",),)
class ExamType(AppModel):
    value = m.TextField(unique=True)
class SubjectExam(AppModel):
    subject = m.ForeignKey(Subject , null=False, related_name="exams", on_delete=m.CASCADE)
    type    = m.ForeignKey(ExamType, null=False, related_name="exams", on_delete=m.CASCADE)
    date    = m.DateField(null=False)
class NoteXStudent(AppModel):
    exam    = m.ForeignKey(SubjectExam, null=False, on_delete=m.CASCADE)
    student = m.ForeignKey(User       , null=False, on_delete=m.CASCADE)
    note    = m.FloatField(null=False)
    class Meta:
        unique_together = (("exam","student",),)

class SubjectXTeacher(AppModel):
    subject = m.ForeignKey(Subject, null=False, related_name="teachers"        , on_delete=m.CASCADE)
    teacher = m.ForeignKey(User   , null=False, related_name="teacher_subjects", on_delete=m.CASCADE)
    class Meta:
        unique_together = (("subject","teacher",),)

class SubjectXStudent(AppModel):
    subject = m.ForeignKey(Subject, null=False, related_name="students"        , on_delete=m.CASCADE)
    student = m.ForeignKey(User   , null=False, related_name="student_subjects", on_delete=m.CASCADE)
    class Meta:
        unique_together = (("subject","student",),)
class ClassAttendance(AppModel):
    subject_x_student = m.ForeignKey(SubjectXStudent, null=False, on_delete=m.CASCADE)
    date              = m.DateField(null=False)
    class Meta:
        unique_together = (("subject_x_student","date",),)

class Form(AppModel):
    title = m.TextField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)
class FormFieldType(AppModel):
    name = m.TextField(unique=True)
class FormField(AppModel):
    form = m.ForeignKey(Form         , null=False, on_delete=m.CASCADE)
    type = m.ForeignKey(FormFieldType, null=False, on_delete=m.CASCADE)
    name = m.TextField(null=False)
    value= m.TextField(null=True ) # Can be null for cases in which person that should complete the form didnt do it or value was not present and not required.
    class Meta:
        unique_together = (("form","name",),)


'''
4 or 5 different apps:

Complete control,
# All data reader,
Account creation and setting,
Teacher side,
Student side,

'''
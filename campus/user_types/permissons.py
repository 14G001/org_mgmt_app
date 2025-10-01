from user.permissons import get_root_user_type_permissons, get_admin_user_type_permissons
from campus.elements import CAMPUS_APP_ELMS_INFO
from django.db.models import Q
from django.db import transaction

def teacher_user_elm_filter(view, request, app):
    teacher = request.user
    return (Q(type__name="student")
        | Q(type__name="teacher",
            teacher_subjects__in=teacher.teacher_subjects.all()))
def teacher_subject_elm_on_create(view, request, app):
    # The following imports should be executing inside this function to avoid circular import errors:
    from app.views.utils.input import get_input_field_values
    from campus.models import Subject, SubjectXTeacher
    with transaction.atomic():
        subject = Subject.objects.create(
            **get_input_field_values(app, view.item_type, view.body))
        SubjectXTeacher.objects.create(
            subject=subject, teacher=request.user)
    return None
def teacher_subject_x_teacher_elm_on_delete(view, request, app):
    # The following imports should be executing inside this function to avoid circular import errors:
    from user.models import User
    from campus.models import Subject, SubjectXTeacher
    subject_x_teacher_id = view.body["id"]
    subject = Subject.objects.filter(teachers_id=subject_x_teacher_id)
    num_of_subject_teachers = (
        User.objects.filter(
        teacher_subjects__subject=subject)
        .count())
    if num_of_subject_teachers < 2:
        with transaction.atomic():
            subject.delete()
            SubjectXTeacher.objects.get(
                id=subject_x_teacher_id).delete()
    return None
def student_user_elm_filter(view, request, app):
    # The following imports should be executing inside this function to avoid circular import errors:
    from campus.models import Subject
    student = request.user
    return (
        Q(student_subjects__subject__in=Subject.objects.filter(students__student=student))
        | Q(teacher_subjects__subject__students__in=student.student_subjects.all()))
APP_USER_TYPE_PERMISSONS = {
    "root" : get_root_user_type_permissons (CAMPUS_APP_ELMS_INFO),
    "admin": get_admin_user_type_permissons(CAMPUS_APP_ELMS_INFO),
    "accounts_and_info_manager": {
        "user_type": {"actions":"cu", "filter": Q(name__in=["teacher","student"]),     },
        "user"     : {"actions":"cu", "filter": Q(type__name__in=["teacher","student"])},
        "address"  : {"actions": "cu"},
        "school"   : {"actions": "cu"},
    },
    "teacher" : {
        "user"             : {"actions":""   , "filter_getter":teacher_user_elm_filter         },
        "address"          : {"actions":""  },
        "school"           : {"actions":""  },
        "subject_type"     : {"actions":"cu"},
        "subject"          : {"actions":"cu" , "on_create":teacher_subject_elm_on_create,      },
        "exam_type"        : {"actions":"cu"},
        "subject_exam"     : {"actions":"cu" , "user_filter":"subject__teachers__teacher"      },
        "subject_x_teacher": {"actions":"cd" ,
            "user_filter"       :"subject__teachers__teacher",
            "actions_user_field":"teacher"                   ,
            "on_delete"         :teacher_subject_x_teacher_elm_on_delete,
        },
        "subject_x_student": {"actions":"cd" , "user_filter":"subject__teachers__teacher"      },
        "note_x_student"   : {"actions":"cu" , "user_filter":"exam__subject__teachers__teacher"},
        "class_attendance" : {"actions":"cd" , "user_filter":"subject_x_student__subject__teachers__teacher"},
    },
    "student" : {
        "user"             : {"actions":"", "filter_getter":student_user_elm_filter    },
        "address"          : {"actions":"", "user_filter":"schools__subjects__students__student"},
        "school"           : {"actions":"", "user_filter":"subjects__students__student"},
        "subject_type"     : {"actions":"", "user_filter":"subjects__students__student"},
        "subject"          : {"actions":"", "user_filter":"students__student"          },
        "exam_type"        : {"actions":"", "user_filter":"exams__subject__students__student"   },
        "subject_exam"     : {"actions":"", "user_filter":"subject__students__student" },
        "subject_x_teacher": {"actions":"", "user_filter":"subject__students__student" },
        "subject_x_student": {"actions":"", "user_filter":"student"                    },
        "note_x_student"   : {"actions":"", "user_filter":"student"                    },
        "class_attendance" : {"actions":"", "user_filter":"subject_x_student__student" },
    },
}

from user.permissons import get_root_user_settings, get_admin_user_settings
from campus.elements import CAMPUS_APP_ELMS_INFO
from django.db.models import Q
from django.apps import apps

def teacher_user_app_elm_filter_getter(request, app):
    teacher = request.user
    return (Q(type__name="student")
        | Q(type__name="teacher",
            teacher_subjects__in=teacher.teacher_subjects.all()))
def student_user_app_elm_filter_getter(request, app):
    subject_model = apps.get_model("campus","Subject") # Importing model in that way is required to avoid circular imports
    student = request.user
    return (
        Q(student_subjects__subject__in=subject_model.objects.filter(students__student=student))
        | Q(teacher_subjects__subject__students__in=student.student_subjects.all()))
def get_campus_app_info():
    return {
        "title":"Campus",
        "user_types": {
            "root" : get_root_user_settings (CAMPUS_APP_ELMS_INFO),
            "admin": get_admin_user_settings(CAMPUS_APP_ELMS_INFO),
            "accounts_and_info_manager" : {
                "title": "Gestor de cuentas y información",
                "permissons": {
                    "user_type": {"actions":"cu", "filter": Q(name__in=["teacher","student"]),     },
                    "user"     : {"actions":"cu", "filter": Q(type__name__in=["teacher","student"])},
                    "address"  : {"actions": "cu"},
                    "school"   : {"actions": "cu"},
                },
                "settings": {
                    "user_type":{"display_at_home":False,},
                },
            },
            "teacher" : {
                "title": "Profesor",
                "permissons": {
                    "user"             : {"actions":"", "filter_getter":teacher_user_app_elm_filter_getter },
                    "address"          : {"actions":""  },
                    "school"           : {"actions":""  },
                    "subject_type"     : {"actions":"cu"},
                    "subject"          : {"actions":"cu"},
                    "exam_type"        : {"actions":"cu"},
                    "subject_exam"     : {"actions":"cu" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_teacher": {"actions":"cu" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_student": {"actions":"cud", "user_filter":"subject__teachers__teacher"      },
                    "note_x_student"   : {"actions":"cu" , "user_filter":"exam__subject__teachers__teacher"},
                    "class_attendance" : {"actions":"cd" , "user_filter":"subject_x_student__subject__teachers__teacher"},
                },
                "settings": {
                    "address"     :{"display_at_home":False,},
                    "subject_type":{"display_at_home":False,},
                },
            },
            "student" : {
                "title": "Alumno",
                "permissons": {
                    "user"             : {"actions":"", "filter_getter":student_user_app_elm_filter_getter  },
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
                "settings": {
                    "address"     :{"display_at_home":False,},
                    "school"      :{"display_at_home":False,},
                    "subject_type":{"display_at_home":False,},
                    "exam_type"   :{"display_at_home":False,},
                },
            },
        }
    }

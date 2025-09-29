from user.permissons import get_admin_permissons
from ensenaxargentina.elements import EXA_APP_ELMS_INFO
from django.db.models import Q

def student_user_app_elm_filter_getter(request, app):
    # TODO: Check how to import the following up propperly without causing circular import or apps not initialized error:
    from ensenaxargentina.models import Subject
    student_subjects = Subject.objects.filter(students__student=request.user)
    return (
        Q(student_subjects__subject__in=student_subjects)
        | Q(teacher_subjects__subject__in=student_subjects))
def get_ensenaxargentina_app_info():
    return {
        "title":"Enseñá X Argentina Campus",
        "user_types": {
            "admin": {
                "title": "Admin",
                "permissons": get_admin_permissons(EXA_APP_ELMS_INFO)
            },
            "accounts_and_info_manager" : {
                "title": "Gestor de cuentas y información",
                "permissons": {
                    "user_type": {"actions":"cu", "app_filter":"app", "filter": Q(name__in=["teacher","student"]),
                        "settings": {"display_at_home":False,}
                    },
                    "user"     : {"actions":"cu", "app_filter":"app", "filter": Q(type__name__in=["teacher","student"])},
                    "address"  : {"actions": "cu"},
                    "school"   : {"actions": "cu"},
                }
            },
            "teacher" : {
                "title": "Profesor",
                "permissons": {
                    "user"             : {"actions":"", "filter": Q(type__name="student")},
                    "address"          : {"actions":"",
                        "settings": {"display_at_home":False,}
                    },
                    "school"           : {"actions":""  },
                    "subject_type"     : {"actions":"cu"},
                    "subject"          : {"actions":"cu"},
                    "exam_type"        : {"actions":"cu"},
                    "subject_exam"     : {"actions":"cu" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_teacher": {"actions":"cu" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_student": {"actions":"cud", "user_filter":"subject__teachers__teacher"      },
                    "note_x_student"   : {"actions":"cu" , "user_filter":"exam__subject__teachers__teacher"},
                    "class_attendance" : {"actions":"cud", "user_filter":"subject_x_student__subject__teachers__teacher"},
                }
            },
            "student" : {
                "title": "Alumno",
                "permissons": {
                    "user"             : {"actions":"", "filter_getter": student_user_app_elm_filter_getter },
                    "address"          : {"actions":"", "user_filter":"schools__subjects__students__student",
                        "settings": {"display_at_home":False,}
                    },
                    "school"           : {"actions":"", "user_filter":"subjects__students__student"},
                    "subject_type"     : {"actions":"", "user_filter":"subjects__students__student"},
                    "subject"          : {"actions":"", "user_filter":"students__student"          },
                    "exam_type"        : {"actions":"", "user_filter":"exams__subject__students__student"   },
                    "subject_exam"     : {"actions":"", "user_filter":"subject__students__student" },
                    "subject_x_teacher": {"actions":"", "user_filter":"subject__students__student" },
                    "subject_x_student": {"actions":"", "user_filter":"student"                    },
                    "note_x_student"   : {"actions":"", "user_filter":"student"                    },
                    "class_attendance" : {"actions":"", "user_filter":"subject_x_student__student" },
                }
            },
        }
    }

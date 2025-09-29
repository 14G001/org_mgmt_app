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
                    "user"   : {"actions":"cru", "filter": Q(type__name__in=["teacher","student"])},
                    "address": {"actions": "cru"},
                    "school" : {"actions": "cru"},
                }
            },
            "teacher" : {
                "title": "Profesor",
                "permissons": {
                    "user"             : {"actions":"r", "filter": Q(type__name="student")},
                    "address"          : {"actions":"r"  },
                    "school"           : {"actions":"r"  },
                    "subject_type"     : {"actions":"cru"},
                    "subject"          : {"actions":"cru"},
                    "exam_type"        : {"actions":"cru"},
                    "subject_exam"     : {"actions":"cru" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_teacher": {"actions":"cru" , "user_filter":"subject__teachers__teacher"      },
                    "subject_x_student": {"actions":"cru" , "user_filter":"subject__teachers__teacher"      },
                    "class_attendance" : {"actions":"crud", "user_filter":"subject_x_student__subject__teachers__teacher"},
                    "note_x_student"   : {"actions":"cru" , "user_filter":"exam__subject__teachers__teacher"},
                }
            },
            "student" : {
                "title": "Alumno",
                "permissons": {
                    "user"             : {"actions":"r", "filter_getter": student_user_app_elm_filter_getter },
                    "address"          : {"actions":"r", "user_filter":"schools__subjects__students__student"},
                    "school"           : {"actions":"r", "user_filter":"subjects__students__student"},
                    "subject_type"     : {"actions":"r", "user_filter":"subjects__students__student"},
                    "subject"          : {"actions":"r", "user_filter":"students__student"          },
                    "exam_type"        : {"actions":"r", "user_filter":"exams__subject__students__student"   },
                    "subject_exam"     : {"actions":"r", "user_filter":"subject__students__student" },
                    "subject_x_teacher": {"actions":"r", "user_filter":"subject__students__student" },
                    "subject_x_student": {"actions":"r", "user_filter":"student"                    },
                    "class_attendance" : {"actions":"r", "user_filter":"subject_x_student__student" },
                    "note_x_student"   : {"actions":"r", "user_filter":"student"                    },
                }
            },
        }
    }
